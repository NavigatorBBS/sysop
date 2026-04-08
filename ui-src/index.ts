import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { KernelMessage } from '@jupyterlab/services';
import { Widget } from '@lumino/widgets';
import DOMPurify from 'dompurify';
import { marked } from 'marked';

const COMMAND_ID = 'sysop:open-panel';
const RESULT_PREFIX = '__SYSOP_RESULT__';
const DEFAULT_CELL_MESSAGE = 'Please discuss the current notebook cell in detail.';

interface CellContext {
  notebook_path: string;
  cell_index: number;
  cell_type: string;
  language: string;
  source: string;
}

interface BridgePayload {
  action: 'chat' | 'clear_history' | 'get_messages' | 'ping';
  message?: string;
  cell_context?: CellContext;
}

interface BridgeResponse {
  ok: boolean;
  reply?: string;
  error?: string;
}

class SysopSidePanel extends Widget {
  private readonly notebookTracker: INotebookTracker;
  private readonly messagesNode: HTMLDivElement;
  private readonly statusNode: HTMLDivElement;
  private readonly inputNode: HTMLTextAreaElement;
  private readonly sendButton: HTMLButtonElement;
  private readonly currentCellButton: HTMLButtonElement;
  private readonly clearButton: HTMLButtonElement;

  constructor(notebookTracker: INotebookTracker) {
    super();
    this.notebookTracker = notebookTracker;
    this.id = 'sysop-jupyterlab-side-panel';
    this.title.label = 'sysop';
    this.title.caption = 'sysop chat';
    this.title.closable = false;
    this.addClass('sysop-SidePanel');

    const body = document.createElement('div');
    body.className = 'sysop-SidePanel-body';

    const header = document.createElement('div');
    header.className = 'sysop-SidePanel-header';

    const title = document.createElement('div');
    title.className = 'sysop-SidePanel-title';
    title.textContent = 'sysop';

    this.statusNode = document.createElement('div');
    this.statusNode.className = 'sysop-SidePanel-status';

    header.append(title, this.statusNode);

    this.messagesNode = document.createElement('div');
    this.messagesNode.className = 'sysop-SidePanel-messages';

    const composer = document.createElement('div');
    composer.className = 'sysop-SidePanel-composer';

    this.inputNode = document.createElement('textarea');
    this.inputNode.className = 'sysop-SidePanel-input jp-mod-styled';
    this.inputNode.placeholder = 'Ask sysop about your notebook or code...';

    const actions = document.createElement('div');
    actions.className = 'sysop-SidePanel-actions';

    this.sendButton = this.createButton('Send', () => {
      void this.sendMessage(false);
    });
    this.currentCellButton = this.createButton('Discuss current cell', () => {
      void this.sendMessage(true);
    });
    this.clearButton = this.createButton('Clear chat', () => {
      void this.clearConversation();
    });

    actions.append(this.sendButton, this.currentCellButton, this.clearButton);

    const helpText = document.createElement('div');
    helpText.className = 'sysop-SidePanel-help';
    helpText.textContent =
      'Use "Discuss current cell" to attach the active cell only for that request.';

    composer.append(this.inputNode, actions, helpText);
    body.append(header, this.messagesNode, composer);
    this.node.append(body);

    this.appendMessage(
      'assistant',
      'Open a notebook with a Python kernel to start a persistent sysop chat.',
      false
    );
    this.updateStatus();
    this.notebookTracker.currentChanged.connect(() => {
      this.updateStatus();
    });
  }

  private createButton(label: string, onClick: () => void): HTMLButtonElement {
    const button = document.createElement('button');
    button.className = 'sysop-SidePanel-button';
    button.textContent = label;
    button.onclick = onClick;
    return button;
  }

  private setBusy(isBusy: boolean, text: string): void {
    this.statusNode.textContent = text;
    this.statusNode.dataset.busy = isBusy ? 'true' : 'false';
    this.sendButton.disabled = isBusy;
    this.currentCellButton.disabled = isBusy;
    this.clearButton.disabled = isBusy;
  }

  private updateStatus(): void {
    const panel = this.notebookTracker.currentWidget;
    if (!panel) {
      this.setBusy(false, 'Open a notebook to start chatting.');
      return;
    }

    const path = panel.context.path || 'Untitled notebook';
    this.setBusy(false, `Ready in ${path}`);
  }

  private appendMessage(
    role: 'user' | 'assistant' | 'error',
    content: string,
    renderMarkdown: boolean,
    contextLabel?: string
  ): void {
    const messageNode = document.createElement('div');
    messageNode.className = `sysop-Message sysop-Message--${role}`;

    const roleNode = document.createElement('div');
    roleNode.className = 'sysop-Message-role';
    roleNode.textContent = role === 'user' ? 'You' : role === 'assistant' ? 'sysop' : 'Error';

    const contentNode = document.createElement('div');
    contentNode.className = 'sysop-Message-content';
    if (renderMarkdown) {
      const rendered = marked.parse(content, { async: false });
      if (typeof rendered !== 'string') {
        throw new Error('sysop markdown rendering unexpectedly returned an async result.');
      }
      contentNode.innerHTML = DOMPurify.sanitize(rendered);
    } else {
      contentNode.textContent = content;
    }

    messageNode.append(roleNode, contentNode);

    if (contextLabel) {
      const contextNode = document.createElement('div');
      contextNode.className = 'sysop-Message-context';
      contextNode.textContent = contextLabel;
      messageNode.append(contextNode);
    }

    this.messagesNode.append(messageNode);
    this.messagesNode.scrollTop = this.messagesNode.scrollHeight;
  }

  private getCurrentNotebookPanel(): NotebookPanel {
    const panel = this.notebookTracker.currentWidget;
    if (!panel) {
      throw new Error('Open a notebook to use sysop.');
    }

    return panel;
  }

  private async getCurrentKernel(panel: NotebookPanel) {
    await panel.sessionContext.ready;
    const kernel = panel.sessionContext.session?.kernel;
    if (!kernel) {
      throw new Error('The current notebook does not have an active kernel.');
    }

    return kernel;
  }

  private getCurrentCellContext(panel: NotebookPanel): CellContext {
    const notebook = panel.content;
    const cell = notebook.activeCell;
    if (!cell) {
      throw new Error('Select a notebook cell before discussing it with sysop.');
    }

    const source = cell.model.sharedModel.getSource();
    return {
      notebook_path: panel.context.path,
      cell_index: notebook.activeCellIndex,
      cell_type: cell.model.type,
      language: cell.model.type === 'code' ? 'python' : 'markdown',
      source
    };
  }

  private async sendMessage(includeCurrentCell: boolean): Promise<void> {
    const panel = this.getCurrentNotebookPanel();
    const rawMessage = this.inputNode.value.trim();
    const message = rawMessage || (includeCurrentCell ? DEFAULT_CELL_MESSAGE : '');
    let contextLabel: string | undefined;
    let cellContext: CellContext | undefined;

    if (!message) {
      this.setBusy(false, 'Enter a message before sending it.');
      return;
    }

    if (includeCurrentCell) {
      cellContext = this.getCurrentCellContext(panel);
      contextLabel = `Attached current cell from ${cellContext.notebook_path} (#${cellContext.cell_index}).`;
    }

    this.appendMessage('user', message, false, contextLabel);
    this.inputNode.value = '';
    this.setBusy(true, includeCurrentCell ? 'Sending with current cell...' : 'Sending...');

    try {
      const response = await this.executeKernelRequest(panel, {
        action: 'chat',
        message,
        cell_context: cellContext
      });

      if (!response.ok) {
        throw new Error(response.error || 'sysop returned an unknown error.');
      }

      this.appendMessage('assistant', response.reply || '', true);
      this.updateStatus();
    } catch (error) {
      const messageText =
        error instanceof Error ? error.message : 'Unexpected error talking to sysop.';
      this.appendMessage('error', messageText, false);
      this.setBusy(false, messageText);
    }
  }

  private async clearConversation(): Promise<void> {
    const panel = this.getCurrentNotebookPanel();
    this.setBusy(true, 'Clearing chat...');

    try {
      const response = await this.executeKernelRequest(panel, { action: 'clear_history' });
      if (!response.ok) {
        throw new Error(response.error || 'Unable to clear the current chat.');
      }

      this.messagesNode.replaceChildren();
      this.appendMessage(
        'assistant',
        'Started a fresh sysop conversation for this kernel.',
        false
      );
      this.updateStatus();
    } catch (error) {
      const messageText =
        error instanceof Error ? error.message : 'Unexpected error clearing the chat.';
      this.appendMessage('error', messageText, false);
      this.setBusy(false, messageText);
    }
  }

  private async executeKernelRequest(
    panel: NotebookPanel,
    payload: BridgePayload
  ): Promise<BridgeResponse> {
    const kernel = await this.getCurrentKernel(panel);
    const payloadText = JSON.stringify(payload);
    const encodedPayload = this.encodeBase64(payloadText);
    const code = this.buildKernelCode(encodedPayload);
    const future = kernel.requestExecute({
      code,
      allow_stdin: false,
      silent: false,
      stop_on_error: false,
      store_history: false
    });

    let stdout = '';
    let executionError = '';

    future.onIOPub = message => {
      switch (message.header.msg_type) {
        case 'stream': {
          const content = message.content as KernelMessage.IStreamMsg['content'];
          stdout += content.text;
          break;
        }
        case 'error': {
          const content = message.content as KernelMessage.IErrorMsg['content'];
          executionError = content.evalue || content.traceback.join('\n');
          break;
        }
        default:
          break;
      }
    };

    await future.done;

    const encodedResult = this.extractEncodedResult(stdout);
    if (!encodedResult) {
      throw new Error(executionError || 'sysop did not return a response.');
    }

    const resultText = this.decodeBase64(encodedResult);
    return JSON.parse(resultText) as BridgeResponse;
  }

  private buildKernelCode(encodedPayload: string): string {
    return [
      'import base64',
      'import json',
      'from IPython import get_ipython',
      'from sysop.jupyter_extension import handle_lab_request',
      '_ipython = get_ipython()',
      'if _ipython is None:',
      '    raise RuntimeError("sysop requires an active IPython kernel.")',
      '_loop_runner = getattr(_ipython, "loop_runner", None)',
      'if not callable(_loop_runner):',
      '    raise RuntimeError("The active IPython kernel does not support async sysop requests.")',
      `_payload = json.loads(base64.b64decode("${encodedPayload}").decode("utf-8"))`,
      'try:',
      '    _result = _loop_runner(handle_lab_request(_ipython, _payload))',
      'except Exception as exc:',
      '    _result = {"ok": False, "error": str(exc)}',
      `_encoded_result = base64.b64encode(json.dumps(_result).encode("utf-8")).decode("ascii")`,
      `print("${RESULT_PREFIX}" + _encoded_result)`
    ].join('\n');
  }

  private extractEncodedResult(stdout: string): string | null {
    const lines = stdout.split(/\r?\n/);
    for (const line of lines) {
      if (line.startsWith(RESULT_PREFIX)) {
        return line.slice(RESULT_PREFIX.length);
      }
    }

    return null;
  }

  private encodeBase64(value: string): string {
    const bytes = new TextEncoder().encode(value);
    let binary = '';
    for (const byte of bytes) {
      binary += String.fromCharCode(byte);
    }

    return window.btoa(binary);
  }

  private decodeBase64(value: string): string {
    const binary = window.atob(value);
    const bytes = Uint8Array.from(binary, character => character.charCodeAt(0));
    return new TextDecoder().decode(bytes);
  }
}

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'sysop-jupyterlab:plugin',
  autoStart: true,
  requires: [ICommandPalette, INotebookTracker],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette, notebookTracker: INotebookTracker) => {
    const panel = new SysopSidePanel(notebookTracker);

    app.commands.addCommand(COMMAND_ID, {
      label: 'Open sysop Chat',
      execute: () => {
        if (!panel.isAttached) {
          app.shell.add(panel, 'right', { rank: 700 });
        }
        app.shell.activateById(panel.id);
      }
    });

    palette.addItem({ command: COMMAND_ID, category: 'sysop' });
    app.commands.execute(COMMAND_ID).catch(reason => {
      console.error('Failed to open sysop side panel.', reason);
    });
  }
};

export default plugin;
