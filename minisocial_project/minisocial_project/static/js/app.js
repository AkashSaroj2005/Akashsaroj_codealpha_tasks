document.addEventListener("DOMContentLoaded", () => {
  // Small client-side polish: autosize post composer and dismiss flash messages.
  document.querySelectorAll(".composer textarea").forEach((area) => {
    const resize = () => { area.style.height = "auto"; area.style.height = Math.min(area.scrollHeight, 220) + "px"; };
    area.addEventListener("input", resize);
    resize();
  });
  document.querySelectorAll(".message").forEach((message) => {
    window.setTimeout(() => {
      message.classList.add("fade-out");
      window.setTimeout(() => message.remove(), 350);
    }, 4500);
  });
  document.querySelectorAll("img").forEach((img) => {
    img.addEventListener("error", () => { img.style.display = "none"; });
  });
});
