# App

The model as an app of interactive panels: every simulation runs in your browser, on the model compiled to WebAssembly by [sbmlsim-core](https://matthiaskoenig.github.io/sbmlsim-core/), with the panels of [sbmlsim-web](https://matthiaskoenig.github.io/sbmlsim-web/). The app is one file, [`hctz_app.html`](hctz_app.html), which needs no server and no network: [open it in its own window](hctz_app.html) or download it and open it from your disk. The factory writes it with the models, so it is the app of the models of this release ([`models/hctz_app.html`](https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_app.html)).

<iframe id="model-app" src="hctz_app.html" title="Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of hydrochlorothiazide, app" style="width: 100%; height: 1200px; border: 0;"></iframe>
<script>
(() => {
  const frame = document.getElementById("model-app");
  const fit = () => {
    const page = frame.contentDocument?.body;
    if (page) frame.style.height = `${page.scrollHeight}px`;
  };
  frame.addEventListener("load", () => {
    fit();
    if (frame.contentDocument) new ResizeObserver(fit).observe(frame.contentDocument.body);
  });
})();
</script>
