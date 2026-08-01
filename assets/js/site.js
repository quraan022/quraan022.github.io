const academySettings = {
  whatsappNumber: "201000000000",
  email: "quraan022@gmail.com",
  siteUrl: "https://quraan022.github.io"
};

function setLanguage(lang) {
  const isArabic = lang === "ar";
  document.documentElement.lang = isArabic ? "ar" : "en";
  document.body.dir = isArabic ? "rtl" : "ltr";
  localStorage.setItem("saraAcademyLang", lang);

  document.querySelectorAll("[data-en][data-ar]").forEach((node) => {
    node.textContent = node.dataset[lang];
  });

  document.querySelectorAll("[data-placeholder-en][data-placeholder-ar]").forEach((node) => {
    node.placeholder = node.dataset[`placeholder${isArabic ? "Ar" : "En"}`];
  });

  document.querySelectorAll("[data-alt-en][data-alt-ar]").forEach((node) => {
    node.alt = node.dataset[`alt${isArabic ? "Ar" : "En"}`];
  });

  document.querySelectorAll(".lang-toggle").forEach((button) => {
    button.textContent = isArabic ? "EN" : "AR";
    button.setAttribute("aria-label", isArabic ? "Switch to English" : "التبديل إلى العربية");
  });
}

function buildWhatsappUrl(message) {
  return `https://wa.me/${academySettings.whatsappNumber}?text=${encodeURIComponent(message)}`;
}

function updateWhatsappLinks() {
  const lang = localStorage.getItem("saraAcademyLang") || "en";
  const defaultMessage = lang === "ar"
    ? "السلام عليكم، أود حجز تجربة مجانية مع Sara Abozeina Quran & Qira'at Academy."
    : "Assalamu Alaikum, I would like to book a free trial with Sara Abozeina Quran & Qira'at Academy.";

  document.querySelectorAll("[data-whatsapp-link]").forEach((link) => {
    link.href = buildWhatsappUrl(defaultMessage);
  });
}

function initNavigation() {
  const menu = document.querySelector(".nav-links");
  const toggle = document.querySelector(".menu-toggle");
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      menu.classList.toggle("open");
    });
  }

  document.querySelectorAll(".lang-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const next = document.documentElement.lang === "ar" ? "en" : "ar";
      setLanguage(next);
      updateWhatsappLinks();
    });
  });
}

function initWhatsApp() {
  updateWhatsappLinks();

  const form = document.querySelector("[data-booking-form]");
  if (!form) return;

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const currentLang = document.documentElement.lang;
    const message = currentLang === "ar"
      ? [
          "السلام عليكم، أود حجز تجربة مجانية.",
          `الاسم: ${data.get("name") || ""}`,
          `واتساب: ${data.get("phone") || ""}`,
          `الدولة: ${data.get("country") || ""}`,
          `العمر: ${data.get("age") || ""}`,
          `المستوى: ${data.get("level") || ""}`,
          `اللغة المفضلة: ${data.get("language") || ""}`,
          `الوقت المناسب: ${data.get("time") || ""}`,
          `ملاحظات: ${data.get("message") || ""}`
        ].join("\n")
      : [
          "Assalamu Alaikum, I would like to book a free trial.",
          `Name: ${data.get("name") || ""}`,
          `WhatsApp: ${data.get("phone") || ""}`,
          `Country: ${data.get("country") || ""}`,
          `Student age: ${data.get("age") || ""}`,
          `Level: ${data.get("level") || ""}`,
          `Preferred language: ${data.get("language") || ""}`,
          `Best time: ${data.get("time") || ""}`,
          `Notes: ${data.get("message") || ""}`
        ].join("\n");
    window.open(buildWhatsappUrl(message), "_blank", "noopener");
  });
}

function initContactLinks() {
  document.querySelectorAll('a[href^="mailto:"], [data-email-link]').forEach((link) => {
    link.href = `mailto:${academySettings.email}`;
  });
  document.querySelectorAll("[data-email-text]").forEach((node) => {
    node.textContent = academySettings.email;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  const saved = localStorage.getItem("saraAcademyLang") || "en";
  setLanguage(saved);
  initWhatsApp();
  initContactLinks();
});
