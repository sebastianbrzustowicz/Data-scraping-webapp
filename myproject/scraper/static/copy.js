function copy() {
    const element = document.querySelector('#textareaID');
    element.select();
    element.setSelectionRange(0, 99999);
    document.execCommand('copy');
  }