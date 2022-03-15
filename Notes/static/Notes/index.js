// Truncate descriptions longer than 50 chars
document.querySelectorAll(".card-text").forEach((p) => {
  let txt = p.textContent;
  if (txt.length > 50) {
    p.textContent = p.textContent.slice(0, 50) + "...";
  }
});
