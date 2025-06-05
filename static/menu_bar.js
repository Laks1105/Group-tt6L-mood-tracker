document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.createElement("nav");
    sidebar.classList.add("sidebar");
    sidebar.innerHTML = `
      <ul>
        <li><a href="/mood">♫ Mood Tracker</a></li>
        <li><a href="/quotes">📖 Quotes</a></li>
        <li><a href="/graph">📊 Statistics</a></li>
        <li><a href="/settings">⚙️ Settings</a></li>
      </ul>
      <div class="logout">
        <a href="/logout">🚶‍♂️ Log out</a>
      </div>
    `;
    document.body.appendChild(sidebar);
  
    const menuButton = document.querySelector(".menu-bar");
    menuButton.addEventListener("click", () => {
      sidebar.classList.toggle("active");
    });
  
    document.addEventListener("click", (e) => {
      if (!sidebar.contains(e.target) && !menuButton.contains(e.target)) {
        sidebar.classList.remove("active");
      }
    });
  
    sidebar.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", function () {
        sidebar.querySelectorAll("a").forEach(a => a.classList.remove("active-link"));
        this.classList.add("active-link");
      });
    });
  });
  