const STORAGE_KEY = "mini_library_books_v1";

function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return { next_id: 1, books: [] };
  try {
    const data = JSON.parse(raw);
    if (!data.next_id || !Array.isArray(data.books)) return { next_id: 1, books: [] };
    return data;
  } catch {
    return { next_id: 1, books: [] };
  }
}

function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function setMsg(text, isError = false) {
  const el = document.getElementById("msg");
  el.textContent = text;
  el.style.color = isError ? "#fca5a5" : "#a7f3d0";
  if (!text) el.style.color = "";
}

function render(books) {
  const tbody = document.getElementById("tbody");
  tbody.innerHTML = "";

  if (books.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="5" style="opacity:.8">No books found.</td>`;
    tbody.appendChild(tr);
    return;
  }

  for (const b of books) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${b.id}</td>
      <td>${escapeHtml(b.title)}</td>
      <td>${escapeHtml(b.author)}</td>
      <td>${b.year}</td>
      <td><button class="smallBtn" data-id="${b.id}">Delete</button></td>
    `;
    tbody.appendChild(tr);
  }
}

function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function getInputs() {
  return {
    title: document.getElementById("title").value.trim(),
    author: document.getElementById("author").value.trim(),
    year: Number(document.getElementById("year").value),
  };
}

function clearInputs() {
  document.getElementById("title").value = "";
  document.getElementById("author").value = "";
  document.getElementById("year").value = "";
}

let state = loadState();

function refresh(query = "") {
  const q = query.trim().toLowerCase();
  const books = q
    ? state.books.filter(b =>
        b.title.toLowerCase().includes(q) || b.author.toLowerCase().includes(q)
      )
    : state.books.slice();

  render(books);
}

document.getElementById("addBtn").addEventListener("click", () => {
  const { title, author, year } = getInputs();

  if (!title) return setMsg("Title cannot be empty.", true);
  if (!author) return setMsg("Author cannot be empty.", true);
  if (!Number.isInteger(year) || year < 0) return setMsg("Year must be a valid integer.", true);

  const book = { id: state.next_id, title, author, year };
  state.books.push(book);
  state.next_id += 1;
  saveState(state);

  clearInputs();
  setMsg(`Added book #${book.id}`);
  refresh(document.getElementById("search").value);
});

document.getElementById("tbody").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-id]");
  if (!btn) return;
  const id = Number(btn.getAttribute("data-id"));

  const before = state.books.length;
  state.books = state.books.filter(b => b.id !== id);

  if (state.books.length !== before) {
    saveState(state);
    setMsg(`Deleted book #${id}`);
    refresh(document.getElementById("search").value);
  }
});

document.getElementById("search").addEventListener("input", (e) => {
  refresh(e.target.value);
});

document.getElementById("resetBtn").addEventListener("click", () => {
  document.getElementById("search").value = "";
  setMsg("");
  refresh("");
});

refresh("");
