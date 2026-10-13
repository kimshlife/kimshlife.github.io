/* Progressive enhancement: the case copy and evidence are already in the HTML. */
(() => {
  const alias = document.body.dataset.edAliases;
  if (alias && location.hash) {
    const routes = JSON.parse(alias);
    const destination = routes[decodeURIComponent(location.hash.slice(1))];
    if (destination) { location.replace(destination); return; }
  }
  document.querySelectorAll('[data-ed-evidence]').forEach(group => {
    const tabs = [...group.querySelectorAll('[role="tab"]')];
    const panels = [...group.querySelectorAll('[role="tabpanel"]')];
    const select = (selected, focus = false) => {
      tabs.forEach((tab, i) => {
        const active = i === selected;
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
        panels[i].hidden = !active;
      });
      if (focus) tabs[selected].focus({preventScroll:true});
    };
    group.querySelector('[role="tablist"]').hidden = false;
    select(0);
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => select(index));
      tab.addEventListener('keydown', event => {
        const step = {ArrowRight:1, ArrowLeft:-1}[event.key];
        if (step || event.key === 'Home' || event.key === 'End') {
          event.preventDefault();
          select(event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length-1 : (index+step+tabs.length)%tabs.length, true);
        }
      });
    });
  });
})();
