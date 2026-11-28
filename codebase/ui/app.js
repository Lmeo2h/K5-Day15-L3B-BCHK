/* Giao diện của bản chạy thử. Mọi chữ từ máy chủ được gắn bằng textContent, không dùng innerHTML. */
"use strict";

const SAMPLES = [
  { ten: "Chuyến cuối tuần", cau: "Mình đi Hà Nội 2 ngày từ thứ Bảy 12/12, 2 triệu, ở phố cổ, thích di tích và chụp ảnh." },
  { ten: "Trúng ngày đóng cửa", cau: "Thứ Hai 14/12 mình ra Hà Nội 2 ngày, 2 triệu rưỡi, rất muốn vào Lăng Bác." },
  { ten: "Ngân sách quá thấp", cau: "Đi Hà Nội 3 ngày từ thứ Sáu 11/12, cả chuyến có 250 nghìn." },
  { ten: "Hạ cánh lúc 0 giờ", cau: "Mình hạ cánh Nội Bài lúc 0 giờ, có xe nào về trung tâm không, giá bao nhiêu?" },
  { ten: "Thiếu thông tin", cau: "Cuối tuần này mình muốn ra Hà Nội chơi, bạn lên lịch giúp." },
  { ten: "Nhờ đặt vé", cau: "Đặt giúp mình vé máy bay ra Hà Nội và thanh toán luôn nhé." },
];
const KHU_NOI = {
  hoan_kiem_old_quarter: "phố cổ", ba_dinh: "Ba Đình", dong_da: "Đống Đa", tay_ho: "Tây Hồ", cau_giay: "Cầu Giấy",
  nam_tu_liem: "Nam Từ Liêm", hai_ba_trung: "Hai Bà Trưng", long_bien: "Long Biên", gia_lam_bat_trang: "Bát Tràng",
  son_tay: "Sơn Tây",
};
const THICH_NOI = { di_tich: "di tích", am_thuc: "ẩm thực", chup_anh: "chụp ảnh", mua_dac_san: "mua đặc sản" };
const THU = ["Chủ nhật", "thứ Hai", "thứ Ba", "thứ Tư", "thứ Năm", "thứ Sáu", "thứ Bảy"];
const TEN_CONG_CU = {
  tra_dia_diem: "Tra điểm và quán đang mở", loc_theo_o: "Lọc nơi mở cửa kịp từng buổi",
  chi_phi_toi_thieu: "Tính mức tiền tối thiểu", kiem_tra_mo_cua: "Kiểm ngày mở cửa",
  kiem_lich_trinh: "Xếp giờ, tính tiền, kiểm vi phạm", va_lich: "Vá điểm trùng hoặc ngày trống",
  chen_diem_muon_di: "Chèn điểm bạn gọi tên", chen_so_thich: "Thêm điểm hợp sở thích",
  ha_chi_phi: "Đổi lựa chọn để vừa ngân sách",
};
const ICONS = {
  sun: "M12 4V2M12 22v-2M4 12H2M22 12h-2M5.6 5.6 4.2 4.2M19.8 19.8l-1.4-1.4M5.6 18.4l-1.4 1.4M19.8 4.2l-1.4 1.4M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z",
  moon: "M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z",
  food: "M4 11h16a8 8 0 0 1-16 0zM8 21h8M9 7c-1-1.5 1-2.500 0-4M14 7c-1-1.5 1-2.500 0-4",
  sight: "M3 21h18M5 21V10M19 21V10M9 21v-7M15 21v-7M2.500 10 12 3l9.500 7z",
  walk: "M13 5a1.500 1.500 0 1 0 0-.1M10 21l2-6-2-3 1-4 3 1.500 2 2.500 2 .5M11 8 8 10v3M13.500 15.500 16 21",
  bike: "M5.500 19a3.500 3.500 0 1 0 0-7 3.500 3.500 0 0 0 0 7zM18.500 19a3.500 3.500 0 1 0 0-7 3.500 3.500 0 0 0 0 7zM5.500 15.500 9 9h6l3.500 6.500M9 9 7.500 7H5M15 9l-1-3h3",
  car: "M5 17H3v-5l2.500-6h13L21 12v5h-2M3 12h18M7 17a2 2 0 1 0 0 .1M17 17a2 2 0 1 0 0 .1M9 17h6",
  check: "M5 12.500 10 17 19 7",
  half: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 3v18",
  help: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM9.500 9.500a2.500 2.500 0 1 1 3.500 2.300c-.8.400-1 .9-1 1.700M12 17v.1",
  warn: "M12 3 2 20h20zM12 10v4M12 17v.1",
  info: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 11v5M12 8v.1",
  pin: "M12 21s-7-6.200-7-11.500a7 7 0 0 1 14 0C19 14.800 12 21 12 21zM12 7a2.500 2.500 0 1 0 0 5 2.500 2.500 0 0 0 0-5z",
  out: "M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5",
  copy: "M9 9h11v11H9zM5 15H4V4h11v1",
  print: "M7 9V3h10v6M7 18H4v-7h16v7h-3M7 14h10v7H7z",
  edit: "M4 20h4L19 9l-4-4L4 16zM13.500 6.500l4 4",
  wallet: "M3 7h15a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3H3zM3 7l12-4v4M17 13.500h.1",
  plane: "M10.500 13 3 10l2-2 8 .5 4-4.500c1.500-1.500 4-1 3 1.500l-4.500 4.500.5 9-2 2-3-7.500-3.500 3.500v3L6 21.500 5 18l-3.500-1L3 15.500h3z",
  shield: "M12 3 4 6v6c0 5 3.500 7.800 8 9 4.500-1.200 8-4 8-9V6zM9 12l2 2 4-4",
  route: "M6 19a2 2 0 1 0 0-.1M18 5a2 2 0 1 0 0-.1M8 19h8a3 3 0 0 0 0-6H8a3 3 0 0 1 0-6h8",
  chip: "M7 7h10v10H7zM10 2v3M14 2v3M10 19v3M14 19v3M2 10h3M2 14h3M19 10h3M19 14h3",
};

const state = { meta: null, busy: false, lastText: "", timer: 0 };
const $ = (selector, root = document) => root.querySelector(selector);
const money = (v) => new Intl.NumberFormat("vi-VN").format(v) + " đ";
const amount = (v) => new Intl.NumberFormat("vi-VN").format(v);
const decimal = (v) => v.toLocaleString("vi-VN", { maximumFractionDigits: 1 });
const reduceMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function h(tag, props, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props || {})) {
    if (value === undefined || value === null || value === false) continue;
    if (key === "class") node.className = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2).toLowerCase(), value);
    else node.setAttribute(key, value === true ? "" : value);
  }
  node.append(...children.flat(Infinity).filter((c) => c !== null && c !== undefined && c !== false));
  return node;
}

function s(tag, attrs, ...children) {
  const node = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [key, value] of Object.entries(attrs || {})) node.setAttribute(key, value);
  node.append(...children.filter(Boolean));
  return node;
}

function icon(name) {
  return s("svg", { class: "ic", viewBox: "0 0 24 24", "aria-hidden": "true" }, s("path", { d: ICONS[name] || ICONS.info }));
}

function link(href, text, iconName) {
  return h("a", { class: "link", href, target: "_blank", rel: "noopener noreferrer" }, iconName && icon(iconName), text);
}

function badge(check) {
  const name = { ok: "check", mot_phan: "half", chua: "help" }[check.muc] || "help";
  return h("span", { class: "badge " + check.muc }, icon(name), check.nhan);
}

function button(text, onClick, kind = "ghost", iconName) {
  return h("button", { type: "button", class: "btn " + kind, onClick }, iconName && icon(iconName), h("span", {}, text));
}

/* Các dòng chữ của câu trả lời, bỏ dòng báo chế độ giả (đã có dải báo ở đầu trang). */
const lines = (text) => String(text || "").split("\n").map((l) => l.trim()).filter((l) => l && !l.startsWith("[CHẾ ĐỘ GIẢ"));

/* ---------- khởi tạo ---------- */
function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  $("#theme").replaceChildren(icon(theme === "dark" ? "sun" : "moon"));
}

function initTheme() {
  let saved = null;
  try { saved = localStorage.getItem("theme"); } catch (e) { /* trình duyệt chặn bộ nhớ: bỏ qua */ }
  applyTheme(saved || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"));
  $("#theme").addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    applyTheme(next);
    try { localStorage.setItem("theme", next); } catch (e) { /* như trên */ }
  });
}

async function loadMeta() {
  const badgeNode = $("#mode");
  try {
    const response = await fetch("/api/meta");
    if (!response.ok) throw new Error(String(response.status));
    state.meta = await response.json();
  } catch (e) {
    badgeNode.textContent = "Mất kết nối";
    badgeNode.className = "mode down";
    return;
  }
  const m = state.meta;
  badgeNode.textContent = m.gia ? "Chế độ giả" : "AI thật · " + m.model;
  badgeNode.className = "mode " + (m.gia ? "fake" : "live");
  $("#fake-banner").hidden = !m.gia;
  $("#data-date").textContent = "Dữ liệu địa điểm đối chiếu ngày " + m.ngay_du_lieu + ". Kiểm lại giờ và giá trước khi đi.";
  $("#q-area").append(...m.khu.map((k) => h("option", { value: k.ma }, k.ten)));
  $("#q-prefs").append(...m.so_thich.map((p) =>
    h("label", {}, h("input", { type: "checkbox", value: p.ma }), h("span", {}, p.ten))));
}

function setText(text, focus = true) {
  const box = $("#yeu-cau");
  box.value = text;
  box.dispatchEvent(new Event("input"));
  if (focus) {
    box.focus({ preventScroll: true });
    $("#form").scrollIntoView({ block: "center", behavior: reduceMotion() ? "auto" : "smooth" });
  }
}

const sampleChips = (items) => items.map((sample) =>
  h("button", { type: "button", class: "chip", title: sample.cau, onClick: () => setText(sample.cau) }, sample.ten));

/* ---------- soạn câu ---------- */
function dayPhrase(value) {
  const [y, m, d] = value.split("-").map(Number);
  const date = new Date(y, m - 1, d);
  const two = (n) => String(n).padStart(2, "0");
  return `${THU[date.getDay()]} ${two(d)}/${two(m)}/${y}`;
}

function sentence({ days, start, budget, people, area, flight, prefs, places }) {
  const parts = [`Mình đi Hà Nội ${days} ngày` + (start ? ` từ ${start}` : "")];
  if (budget) parts.push(`ngân sách ${amount(budget)} đồng`);
  if (people) parts.push(`${people} người`);
  if (area) parts.push(`ở ${KHU_NOI[area] || area}`);
  if (flight) parts.push("đến bằng máy bay");
  if (prefs && prefs.length) parts.push("thích " + prefs.map((p) => THICH_NOI[p] || p).join(" và "));
  if (places && places.length) parts.push("muốn đi " + places.join(", "));
  return parts.join(", ") + ".";
}

function applyQuick() {
  const date = $("#q-date").value;
  setText(sentence({
    days: $('input[name="q-days"]:checked').value,
    start: date ? dayPhrase(date) : "",
    budget: Number($("#q-budget").value) || 0,
    people: Number($("#q-people").value) || 0,
    area: $("#q-area").value,
    flight: $("#q-flight").checked,
    prefs: [...document.querySelectorAll("#q-prefs input:checked")].map((i) => i.value),
  }));
}

/* ---------- gửi yêu cầu ---------- */
function formError(message) {
  const node = $("#form-error");
  node.textContent = message || "";
  node.hidden = !message;
}

function setBusy(busy) {
  state.busy = busy;
  const submit = $("#submit");
  submit.disabled = busy;
  submit.textContent = busy ? "Đang xử lý…" : "Lên lịch";
  document.querySelectorAll("#output button.resend").forEach((b) => { b.disabled = busy; });
}

async function send(raw) {
  if (state.busy) return;
  const text = raw.trim();
  if (!text) {
    formError("Bạn chưa nhập yêu cầu.");
    $("#yeu-cau").focus();
    return;
  }
  if (text.length > 1000) {
    formError("Yêu cầu dài quá 1000 ký tự, bạn rút gọn giúp mình.");
    return;
  }
  formError("");
  state.lastText = text;
  setBusy(true);
  $("#how").hidden = true;
  show(loadingCard());
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 180000);
  try {
    const response = await fetch("/api/lich", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text }),
      signal: controller.signal,
    });
    const data = await response.json().catch(() => null);
    if (!response.ok || !data) {
      show(errorCard((data && data.thong_bao) || "Máy chủ trả lời không đọc được."));
    } else {
      render(data);
    }
  } catch (error) {
    show(errorCard(error.name === "AbortError"
      ? "Chờ quá 3 phút chưa có kết quả. Thử lại sau."
      : "Không gọi được máy chủ trên máy này. Kiểm tra cửa sổ lệnh chạy giao diện còn mở không."));
  } finally {
    clearTimeout(timeout);
    clearInterval(state.timer);
    setBusy(false);
  }
}

function show(...nodes) {
  clearInterval(state.timer);
  hideTip();
  const output = $("#output");
  output.replaceChildren(...nodes.filter(Boolean));
  output.scrollIntoView({ block: "start", behavior: reduceMotion() ? "auto" : "smooth" });
}

function loadingCard() {
  const seconds = h("b", {}, "0");
  const card = h("div", { class: "card state appear", role: "status" },
    h("div", { class: "state-icon" }, h("span", { class: "spinner" })),
    h("div", { class: "state-body" },
      h("h2", {}, "Đang lên lịch"),
      h("p", {}, "Đã chờ ", seconds, " giây. Thường mất vài giây đến khoảng nửa phút."),
      h("ol", { class: "flow", "aria-label": "Trình tự xử lý" },
        ["Model đọc yêu cầu", "Code lọc nơi mở cửa", "Model chọn điểm", "Code tính tiền và kiểm"].map((t) => h("li", {}, t))),
      h("div", { class: "skeleton", "aria-hidden": "true" }, h("i"), h("i"), h("i"))));
  const started = Date.now();
  setTimeout(() => {
    state.timer = setInterval(() => { seconds.textContent = String(Math.round((Date.now() - started) / 1000)); }, 500);
  }, 0);
  return card;
}

function stateCard(iconName, tone, title, ...body) {
  return h("div", { class: "card state appear" },
    h("div", { class: "state-icon " + tone }, icon(iconName)),
    h("div", { class: "state-body" }, h("h2", {}, title), ...body));
}

function errorCard(message) {
  return stateCard("warn", "bad", "Chưa lấy được kết quả",
    h("p", {}, message),
    h("div", { class: "actions" }, h("button", { type: "button", class: "btn primary", onClick: () => send(state.lastText) }, "Thử lại")));
}

function alerts(items) {
  if (!items || !items.length) return null;
  return h("ul", { class: "alerts" }, items.map((text) => {
    const warn = /đóng cửa|không|chưa|vướng/i.test(text);
    return h("li", { class: warn ? "warn" : "" }, icon(warn ? "warn" : "info"), h("span", {}, text));
  }));
}

function render(data) {
  const builders = {
    lich: planView, hoi_lai: askView, khong_du_tien: noMoneyView, khong_xep_duoc: stuckView,
    thong_tin: infoView, tu_choi: refuseView, chua_doc_duoc: unreadView,
  };
  let nodes;
  try {
    nodes = [].concat((builders[data.loai] || plainView)(data.xem || {}, data));
  } catch (error) {
    console.error(error);
    nodes = [plainView({}, data)];
  }
  show(...nodes, runPanel(data));
}

function plainView(view, data) {
  return stateCard("info", "", "Kết quả", lines(data.output).map((l) => h("p", {}, l)));
}

/* ---------- lịch trình ---------- */
function planView(v, data) {
  const days = v.ngay;
  const side = h("aside", { class: "plan-side" });
  const mapHolder = h("section", { class: "card side-card map" });
  const panels = days.map((day, i) => dayPanel(day, i, mapHolder));
  const tabs = h("div", { class: "tabs", role: "tablist", "aria-label": "Chọn ngày" },
    days.map((day, i) => h("button", {
      type: "button", class: "tab", role: "tab", id: "tab-" + i, "aria-controls": "panel-" + i,
      onClick: () => select(i),
      onKeydown: (e) => {
        const step = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
        if (!step) return;
        const next = (i + step + days.length) % days.length;
        select(next);
        tabs.children[next].focus();
      },
    }, h("b", {}, "Ngày " + day.so), h("small", {}, day.thu))));

  function select(index) {
    [...tabs.children].forEach((tab, i) => {
      tab.setAttribute("aria-selected", String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
    });
    panels.forEach((panel, i) => { panel.hidden = i !== index; });
    drawMap(mapHolder, v, days[index], panels[index]);
  }

  const copy = button("Sao chép lịch", async () => {
    const done = await copyText(lines(data.output).length ? data.output : "");
    $("span", copy).textContent = done ? "Đã chép" : "Không chép được";
    setTimeout(() => { $("span", copy).textContent = "Sao chép lịch"; }, 1800);
  }, "ghost small", "copy");

  const head = h("div", { class: "plan-head appear" },
    h("div", {},
      h("h2", {}, `Lịch ${v.so_ngay} ngày của bạn`),
      h("div", { class: "tags" },
        h("span", { class: "tag ok" }, icon("check"), "Qua kiểm giờ mở cửa và trần tiền"),
        h("span", { class: "tag" }, `${v.so_nguoi} người`),
        h("span", { class: "tag" }, icon("pin"), "Ở " + v.khu))),
    h("div", { class: "actions" }, copy,
      button("In / lưu PDF", () => window.print(), "ghost small", "print"),
      button("Sửa yêu cầu", () => setText(state.lastText), "ghost small", "edit")));

  const tips = new Map();
  days.forEach((d) => d.muc.forEach((m) => {
    if (m.diem.loai === "attraction" && m.diem.luu_y) tips.set(m.diem.ten, m.diem.luu_y);
  }));
  const main = h("div", { class: "plan-main appear" }, tabs, panels,
    tips.size ? h("details", { class: "box" }, h("summary", {}, "Lưu ý trước khi đi"),
      h("ul", {}, [...tips].map(([name, note]) => h("li", {}, h("b", {}, name + ": "), note)))) : null,
    h("p", { class: "fine" }, "Tiền xe tính theo đơn giá ",
      v.nguon_di_lai.url ? link(v.nguon_di_lai.url, v.nguon_di_lai.ten) : v.nguon_di_lai.ten,
      ", quãng đường lái xe theo OSRM trên dữ liệu OpenStreetMap, chưa gồm phí nền tảng và giờ cao điểm. " +
      "Không gồm vé máy bay và chỗ ở. Đây là gợi ý, bạn kiểm lại giờ và giá rồi tự quyết."));

  side.append(...[budgetCard(v), v.san_bay && airportCard(v.san_bay, v.so_nguoi), mapHolder].filter(Boolean));
  select(0);
  return [head, alerts(v.ghi_chu), h("div", { class: "plan-grid" }, main, side)];
}

function legRow(leg, label) {
  const name = { "DI-BO": "walk", "GRAB-BIKE": "bike", "GRAB-CAR4": "car" }[leg.ma] || "route";
  return h("li", { class: "leg" }, h("span"), h("span", { class: "rail" }),
    h("span", { class: "leg-text" }, icon(name),
      h("span", {}, `${label}${leg.ten} · ${decimal(leg.km)} km · khoảng ${leg.phut} phút · ${money(leg.tien)}`)));
}

function dayPanel(day, index, mapHolder) {
  const items = [];
  day.muc.forEach((m, i) => {
    const sight = m.diem.loai === "attraction";
    const slotIcon = sight ? (m.o === "toi" ? "moon" : "sight") : "food";
    const hot = (on) => () => {
      row.classList.toggle("hot", on);
      const pin = mapHolder.querySelector(`.pin[data-n="${i + 1}"]`);
      if (pin) pin.classList.toggle("hot", on);
    };
    const row = h("li", { class: "stop " + (sight ? "sight" : "food"), "data-n": i + 1 },
      h("div", { class: "time" }, h("b", {}, m.tu), h("small", {}, m.den)),
      h("div", { class: "rail" }, h("span", { class: "dot" }, String(i + 1))),
      h("div", { class: "place" },
        h("div", { class: "place-top" },
          h("span", { class: "slot" }, icon(slotIcon), m.buoi),
          h("span", { class: "price" + (m.tien ? "" : " free") }, m.tien ? money(m.tien) : "Miễn phí")),
        h("h4", {}, m.diem.ten),
        h("div", { class: "meta" }, h("span", { class: "code" }, m.diem.id), badge(m.diem.kiem),
          link(m.diem.ban_do, "Bản đồ", "pin"),
          m.diem.nguon ? link(m.diem.nguon.url, "Nguồn", "out") : null),
        m.ly_do ? h("p", { class: "why" }, h("b", {}, "Vì sao xếp: "), m.ly_do) : null));
    row.addEventListener("pointerenter", hot(true));
    row.addEventListener("pointerleave", hot(false));
    items.push(legRow(m.di, ""), row);
  });
  items.push(legRow(day.ve, "Về nơi ở: "));
  return h("div", { class: "panel", role: "tabpanel", id: "panel-" + index, "aria-labelledby": "tab-" + index },
    h("div", { class: "day-title" }, h("h3", {}, `Ngày ${day.so}, ${day.thu}`),
      h("span", {}, `Chi trong ngày ${money(day.tong)}, chưa gồm dự phòng`)),
    h("ol", { class: "timeline" }, items));
}

function budgetCard(v) {
  const used = Math.min(100, (v.tong / v.tran) * 100);
  const fill = h("i");
  requestAnimationFrame(() => requestAnimationFrame(() => { fill.style.width = used + "%"; }));
  const parts = v.chi.filter((c) => c.tien > 0);
  const pct = (c) => Math.round((c.tien / v.tong) * 100) + "%";
  const stack = h("div", { class: "stack", role: "img", "aria-label": "Tỷ trọng các khoản chi, số ở bảng bên dưới" },
    parts.map((c) => {
      const segment = h("span", { class: "k-" + c.khoa, tabindex: "0" });
      segment.style.flexGrow = c.tien;
      bindTip(segment, `${c.nhan}: ${money(c.tien)} (${pct(c)})`);
      return segment;
    }));
  return h("section", { class: "card side-card appear" },
    h("h3", {}, icon("wallet"), "Ngân sách"),
    h("div", { class: "total" }, money(v.tong)),
    h("div", { class: "of" }, "tổng dự kiến, trần " + money(v.tran)),
    h("div", { class: "meter", role: "meter", "aria-valuemin": "0", "aria-valuemax": v.tran, "aria-valuenow": v.tong,
      "aria-label": "Đã dùng so với trần" }, fill),
    h("div", { class: "meter-text" }, h("span", {}, `Dùng ${Math.round(used)}% trần`), h("b", {}, "Còn " + money(v.tran - v.tong))),
    h("p", { class: "split-title" }, "Chia theo khoản"),
    stack,
    h("table", { class: "costs" }, h("tbody", {},
      v.chi.map((c) => h("tr", {}, h("td", {}, h("span", { class: "swatch k-" + c.khoa }), c.nhan),
        h("td", { class: "pct" }, pct(c)), h("td", {}, money(c.tien)))),
      h("tr", {}, h("td", {}, "Tổng"), h("td", { class: "pct" }), h("td", {}, money(v.tong))))));
}

/* Sơ đồ vị trí tương đối từ tọa độ, không dùng ảnh bản đồ nên chạy được khi không có mạng. */
function drawMap(holder, v, day, panel) {
  const W = 336, H = 250, PAD = 28;
  const stops = day.muc.map((m, i) => ({ n: i + 1, name: m.diem.ten, food: m.diem.loai !== "attraction", c: m.diem.toa_do }))
    .filter((p) => p.c);
  const all = (v.nha ? [{ n: 0, name: "Nơi ở", c: v.nha }] : []).concat(stops);
  if (!all.length) { holder.hidden = true; return; }
  const kx = Math.cos((all[0].c.lat * Math.PI) / 180);
  const xs = all.map((p) => p.c.lng * kx), ys = all.map((p) => p.c.lat);
  const spanX = Math.max(Math.max(...xs) - Math.min(...xs), 0.008);
  const spanY = Math.max(Math.max(...ys) - Math.min(...ys), 0.008);
  const scale = Math.min((W - 2 * PAD) / spanX, (H - 2 * PAD) / spanY);
  const midX = (Math.max(...xs) + Math.min(...xs)) / 2, midY = (Math.max(...ys) + Math.min(...ys)) / 2;
  all.forEach((p) => {
    p.tx = W / 2 + (p.c.lng * kx - midX) * scale;
    p.ty = H / 2 - (p.c.lat - midY) * scale;
    p.x = p.tx; p.y = p.ty;
  });
  // tách các ghim chồng nhau, vẫn giữ chấm ở vị trí thật
  for (let round = 0; round < 60; round++) {
    for (let a = 0; a < all.length; a++) {
      for (let b = a + 1; b < all.length; b++) {
        const dx = all[b].x - all[a].x || 0.5, dy = all[b].y - all[a].y || 0.5;
        const dist = Math.hypot(dx, dy);
        if (dist >= 25) continue;
        const push = (25 - dist) / 2 / dist;
        all[a].x -= dx * push; all[a].y -= dy * push;
        all[b].x += dx * push; all[b].y += dy * push;
      }
    }
    all.forEach((p) => { p.x = Math.min(W - 14, Math.max(14, p.x)); p.y = Math.min(H - 14, Math.max(14, p.y)); });
  }
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, role: "img",
    "aria-label": "Sơ đồ ngày " + day.so + ": " + stops.map((p) => `${p.n} ${p.name}`).join("; ") });
  for (let x = 42; x < W; x += 42) svg.append(s("line", { class: "grid", x1: x, y1: 0, x2: x, y2: H }));
  for (let y = 42; y < H; y += 42) svg.append(s("line", { class: "grid", x1: 0, y1: y, x2: W, y2: y }));
  const path = (v.nha ? all.concat(all[0]) : all).map((p, i) => `${i ? "L" : "M"}${p.tx.toFixed(1)} ${p.ty.toFixed(1)}`).join("");
  svg.append(s("path", { class: "route", d: path }));
  all.forEach((p) => {
    if (Math.hypot(p.x - p.tx, p.y - p.ty) > 4) {
      svg.append(s("line", { class: "leader", x1: p.tx, y1: p.ty, x2: p.x, y2: p.y }),
        s("circle", { class: "true-dot", cx: p.tx, cy: p.ty, r: 2.5 }));
    }
  });
  // vẽ từ cuối lên để ghim số nhỏ và nơi ở nằm trên
  [...all].reverse().forEach((p) => {
    const mark = p.n === 0
      ? s("g", { class: "home", transform: `translate(${p.x} ${p.y})` },
          s("rect", { x: -11, y: -11, width: 22, height: 22, rx: 6 }), s("path", { d: "M-6 0 0-6 6 0M-4-1v6h8v-6" }))
      : s("g", { class: "pin" + (p.food ? " food" : ""), "data-n": p.n, transform: `translate(${p.x} ${p.y})` },
          s("circle", { r: 11.5 }), s("text", {}, document.createTextNode(String(p.n))));
    bindTip(mark, p.n ? `${p.n}. ${p.name}` : "Điểm xuất phát đại diện cho khu ở");
    if (p.n) {
      const row = panel.querySelector(`.stop[data-n="${p.n}"]`);
      mark.addEventListener("pointerenter", () => row && row.classList.add("hot"));
      mark.addEventListener("pointerleave", () => row && row.classList.remove("hot"));
      mark.addEventListener("click", () => row && row.scrollIntoView({ block: "center", behavior: reduceMotion() ? "auto" : "smooth" }));
    }
    svg.append(mark);
  });
  const kmPerPx = 111.32 / scale;
  const km = [10, 5, 2, 1, 0.5, 0.2].find((k) => k / kmPerPx <= 90) || 0.2;
  svg.append(s("g", { class: "scale" },
    s("line", { x1: 10, y1: H - 10, x2: 10 + km / kmPerPx, y2: H - 10 }),
    s("text", { x: 10, y: H - 16 }, document.createTextNode(decimal(km) + " km"))));
  holder.hidden = false;
  holder.replaceChildren(
    h("h3", {}, icon("route"), `Đường đi ngày ${day.so}`), svg,
    day.tuyen ? h("a", { class: "btn ghost small", href: day.tuyen, target: "_blank", rel: "noopener noreferrer" },
      icon("out"), "Chỉ đường cả ngày trên Google Maps") : null,
    h("p", { class: "note" }, "Sơ đồ chỉ cho vị trí tương đối, đường nối thẳng không phải đường đi thật. " +
      "Google Maps trên trình duyệt điện thoại nhận tối đa 3 điểm giữa."));
}

function airportCard(a, people) {
  return h("section", { class: "card side-card airport" },
    h("h3", {}, icon("plane"), "Từ và về Nội Bài"),
    h("p", {}, a.ten),
    h("span", { class: "price" }, money(a.mot_chieu) + " một chiều" + (people > 1 ? ` cho ${people} người` : "")),
    h("p", {}, "Giờ chạy: " + a.gio_chay + " · ", h("span", { class: "code" }, a.id)),
    h("p", { class: "fine" }, "Chưa tính giờ hạ cánh của bạn. Kiểm xe còn chạy vào giờ đó."));
}

/* ---------- hỏi lại ---------- */
function askView(v, data) {
  const body = lines(data.output).map((l) => h("p", {}, l));
  if (v.qua_so_ngay) {
    const shorter = /\d+\s*ngày/i.test(state.lastText)
      ? state.lastText.replace(/\d+\s*ngày/gi, "3 ngày")
      : state.lastText.replace(/[.\s]*$/, "") + ". Mình chỉ cần lịch 3 ngày.";
    return stateCard("help", "warn", "Lịch chỉ xếp được tối đa 3 ngày", body,
      h("div", { class: "actions" },
        h("button", { type: "button", class: "btn primary resend", onClick: () => { setText(shorter, false); send(shorter); } }, "Xếp 3 ngày đầu"),
        button("Tự sửa yêu cầu", () => setText(state.lastText))));
  }
  const need = new Set(v.thieu);
  const fields = {
    so_ngay: () => h("label", { class: "field" }, "Số ngày",
      h("select", { name: "so_ngay" }, [1, 2, 3].map((n) => h("option", { value: n, selected: n === 2 }, n + " ngày")))),
    ngay: () => h("label", { class: "field" }, "Ngày bắt đầu", h("input", { type: "date", name: "ngay" })),
    ngan_sach: () => h("label", { class: "field" }, "Ngân sách cả chuyến (đồng)",
      h("input", { type: "number", name: "ngan_sach", min: "1", step: "50000", inputmode: "numeric", placeholder: "Ví dụ 2000000" })),
    so_nguoi: () => h("label", { class: "field" }, "Số người đi",
      h("input", { type: "number", name: "so_nguoi", min: "1", max: "20", inputmode: "numeric", placeholder: "Ví dụ 2" })),
  };
  const warning = h("p", { class: "form-error", role: "alert", hidden: true });
  const form = h("form", {
    novalidate: true,
    onSubmit: (event) => {
      event.preventDefault();
      const value = (name) => (form.elements[name] ? form.elements[name].value.trim() : "");
      const missing = [...need].filter((name) => fields[name] && !(name === "ngay" ? value(name) : Number(value(name)) > 0));
      warning.hidden = !missing.length;
      if (missing.length) {
        warning.textContent = "Bạn điền đủ các ô còn trống nhé.";
        form.elements[missing[0]].focus();
        return;
      }
      const extra = [];
      if (need.has("so_ngay")) extra.push(`Đi ${value("so_ngay")} ngày.`);
      if (need.has("ngay")) extra.push(`Bắt đầu từ ${dayPhrase(value("ngay"))}.`);
      if (need.has("ngan_sach")) extra.push(`Ngân sách ${amount(Number(value("ngan_sach")))} đồng.`);
      if (need.has("so_nguoi")) extra.push(`Đi ${value("so_nguoi")} người.`);
      const text = state.lastText.replace(/([^.!?])\s*$/, "$1.") + " " + extra.join(" ");
      setText(text, false);
      send(text);
    },
  },
    h("div", { class: "ask-grid" }, [...need].map((name) => fields[name] && fields[name]())),
    warning,
    h("div", { class: "actions" }, h("button", { type: "submit", class: "btn primary resend" }, "Bổ sung và lên lịch")));
  return stateCard("help", "", "Cho mình thêm vài thông tin", body, form);
}

/* ---------- không đủ tiền, không xếp được ---------- */
function suggestions(rb, budget, extra = []) {
  const base = { days: rb.so_ngay, start: rb.thu, budget: rb.ngan_sach, people: rb.so_nguoi, area: rb.khu,
    flight: rb.di_may_bay, prefs: rb.so_thich, places: rb.diem_muon_di };
  const hint = h("p", { class: "note" }, "Bấm một gợi ý để soạn lại câu ở ô trên, rồi bấm Lên lịch.");
  const buttons = [button(`Thử với ${money(budget)}`, () => setText(sentence({ ...base, budget })), "primary")];
  if (rb.so_ngay > 1) buttons.push(button("Giảm còn 1 ngày", () => setText(sentence({ ...base, days: 1 }))));
  extra.forEach(([label, change]) => buttons.push(button(label, () => setText(sentence({ ...base, ...change })))));
  buttons.push(button("Tự sửa yêu cầu", () => setText(state.lastText)));
  return [h("div", { class: "actions" }, buttons), hint];
}

const roundUp = (v, step = 50000) => Math.ceil(v / step) * step;

function noMoneyView(v, data) {
  const rb = v.rang_buoc;
  const max = Math.max(rb.ngan_sach, v.toi_thieu);
  const row = (label, value) => {
    const bar = h("i");
    bar.style.width = (value / max) * 70 + "%";
    return h("div", {}, h("span", {}, label), h("span", { class: "bar" }, bar, h("b", {}, money(value))));
  };
  return [alerts(v.ghi_chu), stateCard("wallet", "warn", "Chưa xếp được trong mức tiền này",
    h("div", { class: "compare" }, row("Trần của bạn", rb.ngan_sach), row("Tối thiểu theo dữ liệu", v.toi_thieu)),
    lines(data.output).filter((l) => !(v.ghi_chu || []).includes(l)).map((l) => h("p", {}, l)),
    suggestions(rb, roundUp(v.toi_thieu * 1.6)))];
}

function stuckView(v) {
  const rb = v.rang_buoc;
  const extra = rb.diem_muon_di.length ? [["Bỏ các điểm gọi tên", { places: [] }]] : [];
  return [alerts(v.ghi_chu), stateCard("warn", "warn", "Chưa có lịch nào đạt mọi ràng buộc",
    h("p", {}, "Mình không đưa ra lịch còn vi phạm. Chỗ đang vướng:"),
    h("ul", {}, v.vuong.map((w) => h("li", {}, w))),
    suggestions(rb, roundUp(rb.ngan_sach * 1.3), extra))];
}

/* ---------- thông tin, từ chối ---------- */
function infoView(v, data) {
  const trips = v.chuyen.map((t) => h("article", { class: "card info-card" },
    h("h3", {}, t.ten),
    h("div", { class: "big" }, t.gia_min === t.gia_max ? money(t.gia_min) : `${amount(t.gia_min)} đến ${money(t.gia_max)}`,
      h("small", {}, " / " + t.don_vi)),
    h("dl", {}, h("dt", {}, "Giờ chạy"), h("dd", {}, t.gio), t.tuyen ? [h("dt", {}, "Tuyến"), h("dd", {}, t.tuyen)] : null),
    h("div", { class: "meta" }, h("span", { class: "code" }, t.id), badge(t.kiem), t.nguon ? link(t.nguon.url, "Nguồn", "out") : null)));
  const places = v.diem.map((p) => h("article", { class: "card info-card" },
    h("h3", {}, p.ten),
    h("dl", {}, h("dt", {}, "Giờ mở"), h("dd", {}, p.gio),
      h("dt", {}, "Ngày đóng"), h("dd", {}, p.ngay_dong.join(", ") || "Không có ngày cố định"),
      h("dt", {}, "Giá"), h("dd", {}, p.gia)),
    h("div", { class: "meta" }, h("span", { class: "code" }, p.id), badge(p.kiem), link(p.ban_do, "Bản đồ", "pin"),
      p.nguon ? link(p.nguon.url, "Nguồn", "out") : null)));
  const unknown = v.khong_co.map((name) => `${name}: không có dữ liệu, mình không đoán giá hay giờ.`);
  const notes = alerts([...(v.ghi_chu || []), ...v.canh_bao, ...unknown]);
  if (!trips.length && !places.length) {
    return [notes, notes ? null : plainView(v, data)];
  }
  return [h("div", { class: "plan-head" }, h("h2", {}, "Thông tin bạn hỏi")), notes,
    h("div", { class: "info-grid appear" }, trips, places),
    h("p", { class: "fine" }, `Giá và giờ là tham khảo, đối chiếu ngày ${state.meta ? state.meta.ngay_du_lieu : ""}. Kiểm lại trước khi đi.`)];
}

function refuseView(v, data) {
  return stateCard("shield", "warn", "Phần này mình không làm",
    lines(data.output).map((l) => h("p", {}, l)),
    h("p", {}, h("b", {}, "Mình làm được: "), "lịch tham quan Hà Nội 1 đến 3 ngày, dự toán chi phí, giờ mở cửa và xe từ Nội Bài."),
    h("div", { class: "samples" }, sampleChips([SAMPLES[0], SAMPLES[3]])));
}

function unreadView(v, data) {
  return stateCard("help", "warn", "Mình chưa đọc được yêu cầu",
    lines(data.output).map((l) => h("p", {}, l)),
    h("div", { class: "actions" }, button("Điền theo từng mục", () => {
      $("#quick").open = true;
      $("#quick").scrollIntoView({ block: "center" });
      $("#q-date").focus({ preventScroll: true });
    }, "primary")));
}

/* ---------- thông tin lượt chạy ---------- */
function runPanel(data) {
  const run = data.luot;
  let calls = 0;
  const steps = run.buoc.map((step) => {
    let who = ["log", "Ghi"], title = step.text || "";
    let detail = "";
    if (step.kind === "model") {
      who = ["ai", "AI"];
      title = calls++ === 0 ? "Model đọc yêu cầu" : "Model chọn điểm và thứ tự";
      detail = `${amount(step.tokens_in)} + ${amount(step.tokens_out)} token · ${decimal(step.latency_s)} s`;
    } else if (step.kind === "tool") {
      who = ["code", "Code"];
      title = TEN_CONG_CU[step.name] || step.name;
    }
    return h("li", {}, h("span", { class: "who " + who[0] }, who[1]), h("span", {}, title + (step.loi ? " (lỗi)" : "")),
      h("small", {}, detail));
  });
  const tile = (label, value) => h("div", {}, h("span", {}, label), h("b", {}, value));
  return h("details", { class: "box run" },
    h("summary", {}, icon("chip"), "Cách ra kết quả này",
      h("small", {}, `${run.model || "không gọi model"} · ${decimal(run.giay)} giây`)),
    h("div", { class: "tiles" }, tile("Lần gọi model", String(run.goi_model)), tile("Lần gọi công cụ", String(run.goi_cong_cu)),
      tile("Token vào", amount(run.token_vao)), tile("Token ra", amount(run.token_ra))),
    h("ol", { class: "steps" }, steps),
    h("details", { class: "raw" }, h("summary", {}, "Bản chữ đầy đủ"), h("pre", {}, data.output)));
}

/* ---------- tiện ích ---------- */
async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (e) {
    const area = h("textarea", { class: "sr-only" });
    area.value = text;
    document.body.append(area);
    area.select();
    const done = document.execCommand("copy");
    area.remove();
    return done;
  }
}

function bindTip(node, text) {
  const tip = $("#tip");
  const place = (x, y) => {
    tip.textContent = text;
    tip.hidden = false;
    const box = tip.getBoundingClientRect();
    tip.style.left = Math.max(8, Math.min(window.innerWidth - box.width - 8, x - box.width / 2)) + "px";
    tip.style.top = Math.max(8, y - box.height - 12) + "px";
  };
  node.addEventListener("pointermove", (e) => place(e.clientX, e.clientY));
  node.addEventListener("pointerleave", hideTip);
  node.addEventListener("focus", () => { const r = node.getBoundingClientRect(); place(r.left + r.width / 2, r.top); });
  node.addEventListener("blur", hideTip);
}

function hideTip() {
  $("#tip").hidden = true;
}

function init() {
  initTheme();
  $("#samples").append(...sampleChips(SAMPLES));
  $("#q-date").value = "2026-12-05";
  $("#q-apply").addEventListener("click", applyQuick);
  const box = $("#yeu-cau");
  box.addEventListener("input", () => {
    $("#count").textContent = box.value.length + "/1000";
    formError("");
  });
  box.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      send(box.value);
    }
  });
  $("#form").addEventListener("submit", (e) => {
    e.preventDefault();
    send(box.value);
  });
  // bản in: mở sẵn các khung gấp để lưu ý không bị mất
  window.addEventListener("beforeprint", () => document.querySelectorAll("#output details.box:not(.run)").forEach((d) => { d.open = true; }));
  window.addEventListener("scroll", () => {
    // cuộn do chuyển tiêu điểm bàn phím: đặt lại chú thích theo vị trí mới, còn lại thì ẩn
    const focused = document.activeElement;
    if (focused && focused.matches(".stack span")) focused.dispatchEvent(new FocusEvent("focus"));
    else hideTip();
  }, { passive: true });
  loadMeta();
}

init();
