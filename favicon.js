document.addEventListener("DOMContentLoaded", function() {
    const websiteLinks = document.querySelectorAll('.website-link');
    websiteLinks.forEach(link => {
      const faviconUrl = `https://www.google.com/s2/favicons?domain=${link.href}`;
      const imgElement = link.previousElementSibling;
      imgElement.src = faviconUrl;
    });
  });