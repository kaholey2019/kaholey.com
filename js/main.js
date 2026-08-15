(() => {
  "use strict";

  const root = document.documentElement;
  root.classList.add("js-ready");

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  const progress = document.createElement("div");
  progress.className = "scroll-progress";
  progress.setAttribute("aria-hidden", "true");
  document.body.prepend(progress);

  const updateProgress = () => {
    const max = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const value = max > 0 ? window.scrollY / max : 0;
    progress.style.transform = `scaleX(${value})`;
  };
  updateProgress();
  window.addEventListener("scroll", updateProgress, { passive: true });
  window.addEventListener("resize", updateProgress);

  const backToTop = document.createElement("button");
  backToTop.className = "back-to-top";
  backToTop.type = "button";
  backToTop.setAttribute("aria-label", "Retour en haut");
  backToTop.innerHTML = '<svg class="icon" aria-hidden="true"><use href="assets/icons.svg#icon-arrow-up"></use></svg>';
  document.body.appendChild(backToTop);

  const onScrollUI = () => backToTop.classList.toggle("is-visible", window.scrollY > 600);
  onScrollUI();
  window.addEventListener("scroll", onScrollUI, { passive: true });
  backToTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: reducedMotion.matches ? "auto" : "smooth" });
  });

  const header = document.getElementById("site-header");
  const nav = document.getElementById("site-nav");
  const navToggle = document.getElementById("nav-toggle");

  if (navToggle && nav) {
    const setMenu = (open) => {
      navToggle.setAttribute("aria-expanded", String(open));
      navToggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
      nav.classList.toggle("is-open", open);
      if (header) header.classList.toggle("menu-open", open);
    };

    navToggle.addEventListener("click", () => setMenu(!nav.classList.contains("is-open")));
    nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => setMenu(false)));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") setMenu(false);
    });
  }

  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  if (window.matchMedia("(pointer: fine)").matches && !reducedMotion.matches) {
    document.querySelectorAll(".btn").forEach((button) => {
      button.addEventListener("pointermove", (event) => {
        const rect = button.getBoundingClientRect();
        const x = (event.clientX - rect.left - rect.width / 2) / rect.width;
        const y = (event.clientY - rect.top - rect.height / 2) / rect.height;
        button.style.transform = `translate(${x * 7}px, ${y * 7}px)`;
      });
      button.addEventListener("pointerleave", () => {
        button.style.transform = "";
      });
    });

    document.querySelectorAll(".featured-card, .home-gallery-card").forEach((card) => {
      card.addEventListener("pointermove", (event) => {
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - 0.5;
        const y = (event.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = `perspective(900px) rotateX(${(-y * 4).toFixed(2)}deg) rotateY(${(x * 4).toFixed(2)}deg) scale(1.015)`;
      });
      card.addEventListener("pointerleave", () => {
        card.style.transform = "";
      });
    });
  }

  const heroRotator = document.getElementById("hero-rotator");
  if (heroRotator && !reducedMotion.matches) {
    const words = ["grands espaces", "lumières rares", "rivages du Bénin", "villes suspendues"];
    let wordIndex = 0;
    window.setInterval(() => {
      heroRotator.style.opacity = "0";
      window.setTimeout(() => {
        wordIndex = (wordIndex + 1) % words.length;
        heroRotator.textContent = words[wordIndex];
        heroRotator.style.opacity = "1";
      }, 220);
    }, 3400);
  }

  const filterButtons = Array.from(document.querySelectorAll(".filter-btn"));
  const cards = Array.from(document.querySelectorAll(".work-card, .project-card"));
  let visibleCards = [];

  const applyFilter = (filter) => {
    visibleCards = cards.filter((card) => {
      const show = filter === "all" || card.dataset.category === filter;
      card.classList.toggle("is-hidden", !show);
      return show;
    });

    filterButtons.forEach((button) => {
      const active = button.dataset.filter === filter;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
  };

  if (filterButtons.length) {
    filterButtons.forEach((button) => {
      button.addEventListener("click", () => applyFilter(button.dataset.filter));
    });
    const requestedFilter = new URLSearchParams(window.location.search).get("filter");
    const initialFilter =
      requestedFilter && filterButtons.some((button) => button.dataset.filter === requestedFilter)
        ? requestedFilter
        : "all";
    applyFilter(initialFilter);
  } else {
    visibleCards = cards;
  }

  const lightbox = document.getElementById("lightbox");
  if (lightbox) {
    const lightboxImage = document.getElementById("lightbox-image");
    const lightboxTitle = document.getElementById("lightbox-title");
    const lightboxContext = document.getElementById("lightbox-context");
    let lightboxIndex = 0;

    const openLightbox = (index) => {
      if (!visibleCards.length) return;
      const safeIndex = (index + visibleCards.length) % visibleCards.length;
      const card = visibleCards[safeIndex];
      const image = card.querySelector("img");
      lightboxImage.src = card.dataset.image || image.src;
      lightboxImage.alt = image.alt;
      lightboxTitle.textContent = card.dataset.title;
      lightboxContext.textContent = card.dataset.context;
      lightboxIndex = safeIndex;
      if (!lightbox.open) lightbox.showModal();
    };

    const closeLightbox = () => {
      if (lightbox.open) lightbox.close();
    };

    cards.forEach((card) => {
      card.addEventListener("click", () => {
        const index = visibleCards.indexOf(card);
        if (index !== -1) openLightbox(index);
      });
    });

    document.getElementById("lightbox-close")?.addEventListener("click", closeLightbox);
    document.getElementById("lightbox-prev")?.addEventListener("click", () => openLightbox(lightboxIndex - 1));
    document.getElementById("lightbox-next")?.addEventListener("click", () => openLightbox(lightboxIndex + 1));

    lightbox.addEventListener("click", (event) => {
      if (event.target === lightbox) closeLightbox();
    });

    document.addEventListener("keydown", (event) => {
      if (!lightbox.open) return;
      if (event.key === "ArrowRight") openLightbox(lightboxIndex + 1);
      if (event.key === "ArrowLeft") openLightbox(lightboxIndex - 1);
    });
  }

  const revealElements = Array.from(document.querySelectorAll("[data-reveal]"));
  if ("IntersectionObserver" in window && revealElements.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealElements.forEach((element) => observer.observe(element));
  } else {
    revealElements.forEach((element) => element.classList.add("is-visible"));
  }

  const counters = Array.from(document.querySelectorAll("[data-count]"));
  const animateCounter = (element) => {
    const target = Number(element.dataset.count);
    const suffix = element.dataset.suffix || "";
    if (reducedMotion.matches) {
      element.textContent = `${target}${suffix}`;
      return;
    }
    const duration = 1100;
    const start = performance.now();
    const tick = (now) => {
      const progressValue = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progressValue, 3);
      element.textContent = `${Math.round(target * eased)}${suffix}`;
      if (progressValue < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  if ("IntersectionObserver" in window && counters.length) {
    const counterObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            counterObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((element) => counterObserver.observe(element));
  } else {
    counters.forEach(animateCounter);
  }

  const form = document.getElementById("contact-form");
  if (form) {
    const status = document.getElementById("form-status");
    const inputs = {
      name: document.getElementById("name"),
      email: document.getElementById("email"),
      message: document.getElementById("message"),
    };
    const errorMessages = {
      name: document.getElementById("name-error"),
      email: document.getElementById("email-error"),
      message: document.getElementById("message-error"),
    };

    const setFieldError = (field, message) => {
      field.setAttribute("aria-invalid", "true");
      field.classList.add("is-invalid");
      if (errorMessages[field.id]) errorMessages[field.id].textContent = message;
    };

    const clearFieldError = (field) => {
      field.removeAttribute("aria-invalid");
      field.classList.remove("is-invalid");
      if (errorMessages[field.id]) errorMessages[field.id].textContent = "";
    };

    Object.keys(inputs).forEach((key) => {
      inputs[key].addEventListener("input", () => {
        if (inputs[key].value.trim()) clearFieldError(inputs[key]);
      });
    });

    const validate = () => {
      let valid = true;
      if (inputs.name.value.trim().length < 2) {
        setFieldError(inputs.name, "Indiquez votre nom.");
        valid = false;
      }
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(inputs.email.value.trim())) {
        setFieldError(inputs.email, "Indiquez une adresse email valide.");
        valid = false;
      }
      if (inputs.message.value.trim().length < 10) {
        setFieldError(inputs.message, "Décrivez votre projet en quelques mots.");
        valid = false;
      }
      return valid;
    };

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      Object.keys(inputs).forEach((key) => clearFieldError(inputs[key]));

      if (!validate()) {
        status.textContent = "Veuillez corriger les champs indiqués.";
        status.className = "form-status is-error";
        const firstInvalid = form.querySelector("[aria-invalid='true']");
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      const type = document.getElementById("type").value;
      const date = document.getElementById("date").value;
      const subject = `Demande de projet : ${type}`;
      const body = [
        `Nom : ${inputs.name.value.trim()}`,
        `Email : ${inputs.email.value.trim()}`,
        `Type de projet : ${type}`,
        date ? `Date souhaitée : ${date}` : "Date souhaitée : à définir",
        "",
        inputs.message.value.trim(),
      ].join("\n");

      window.location.href = `mailto:kaholey@126.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      form.reset();
      status.textContent = "Merci ! Votre demande est prête dans votre messagerie.";
      status.className = "form-status is-success";
    });
  }
})();
