(() => {
  const cfg = window.SSKETCH_CONFIG || {};

  // ---------- Download ----------
  document.querySelectorAll("[data-download]").forEach((a) => {
    if (cfg.downloadLabel) {
      const label = a.querySelector("[data-download-label]");
      if (label) label.textContent = cfg.downloadLabel;
    }

    if (cfg.downloadUrl) {
      a.href = cfg.downloadUrl;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
    } else {
      a.href = "#download";
      a.setAttribute("aria-disabled", "true");
      a.addEventListener("click", (e) => {
        e.preventDefault();
        document.querySelector("#download")?.scrollIntoView({behavior:"smooth"});
        const notice = document.querySelector("#download-notice");
        if (notice) {
          notice.hidden = false;
          setTimeout(() => notice.classList.add("show"), 10);
        }
      });
    }
  });

  // ---------- YouTube ----------
  function extractYouTubeId(url) {
    if (!url) return "";
    try {
      const u = new URL(url);
      if (u.hostname.includes("youtu.be")) {
        return u.pathname.split("/").filter(Boolean)[0] || "";
      }
      if (u.hostname.includes("youtube.com")) {
        if (u.pathname.startsWith("/embed/")) return u.pathname.split("/embed/")[1]?.split("/")[0] || "";
        if (u.pathname.startsWith("/shorts/")) return u.pathname.split("/shorts/")[1]?.split("/")[0] || "";
        return u.searchParams.get("v") || "";
      }
    } catch (_) {}
    // ID만 직접 넣어도 동작
    return /^[A-Za-z0-9_-]{6,}$/.test(url) ? url : "";
  }

  const trailerHost = document.querySelector("#trailer-host");
  const youtubeId = extractYouTubeId(cfg.trailerYoutubeUrl || "");
  if (trailerHost && youtubeId) {
    trailerHost.innerHTML = `
      <iframe
        src="https://www.youtube-nocookie.com/embed/${youtubeId}?rel=0"
        title="SSketch 게임 트레일러"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen>
      </iframe>`;
    trailerHost.classList.add("has-video");
  }

  // ---------- Screenshot gallery ----------
  const grid = document.querySelector("#screenshot-grid");
  if (grid && Array.isArray(cfg.screenshots)) {
    grid.innerHTML = "";
    cfg.screenshots.forEach((shot, idx) => {
      const button = document.createElement("button");
      button.className = "shot-card";
      button.type = "button";
      button.dataset.index = idx;
      button.setAttribute("aria-label", `${shot.caption || `스크린샷 ${idx+1}`} 크게 보기`);
      button.innerHTML = `
        <img src="${shot.src}" alt="${shot.alt || ""}" loading="lazy" decoding="async">
        <span>${shot.caption || ""}</span>
      `;
      grid.appendChild(button);
    });
  }

  // ---------- Lightbox ----------
  const lightbox = document.querySelector("#lightbox");
  const lightboxImg = document.querySelector("#lightbox-img");
  const lightboxCaption = document.querySelector("#lightbox-caption");

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove("open");
    document.body.classList.remove("no-scroll");
  }

  document.addEventListener("click", (e) => {
    const card = e.target.closest(".shot-card");
    if (card && lightbox && Array.isArray(cfg.screenshots)) {
      const shot = cfg.screenshots[Number(card.dataset.index)];
      if (!shot) return;
      lightboxImg.src = shot.src;
      lightboxImg.alt = shot.alt || "";
      lightboxCaption.textContent = shot.caption || "";
      lightbox.classList.add("open");
      document.body.classList.add("no-scroll");
    }

    if (e.target.closest("[data-close-lightbox]") || e.target === lightbox) {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeLightbox();
  });

  // ---------- Header ----------
  const header = document.querySelector(".site-header");
  const onScroll = () => header?.classList.toggle("scrolled", window.scrollY > 18);
  onScroll();
  window.addEventListener("scroll", onScroll, {passive:true});

  // ---------- Mobile menu ----------
  const menuBtn = document.querySelector("#menu-btn");
  const navLinks = document.querySelector("#nav-links");
  menuBtn?.addEventListener("click", () => {
    const open = navLinks.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", String(open));
  });
  navLinks?.querySelectorAll("a").forEach(a => a.addEventListener("click", () => {
    navLinks.classList.remove("open");
    menuBtn?.setAttribute("aria-expanded", "false");
  }));
})();
