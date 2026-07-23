(function () {
  const animateCounters = () => {
    const elements = document.querySelectorAll("[data-count]");
    elements.forEach((el) => {
      const raw = el.getAttribute("data-count") || "0";
      const target = parseFloat(raw) || 0;
      const isNumber = !String(raw).includes(".");
      let start = 0;
      const duration = 900;
      const startTime = performance.now();

      const tick = (now) => {
        const progress = Math.min((now - startTime) / duration, 1);
        const current = target * progress;
        el.textContent = isNumber ? Math.round(current).toString() : current.toFixed(0);
        if (progress < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  };

  const setupCopyButtons = () => {
    document.querySelectorAll("[data-copy]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const text = btn.getAttribute("data-copy");
        try {
          await navigator.clipboard.writeText(text);
          if (window.Swal) Swal.fire({ icon: "success", title: "Disalin", text: "Nomor rekening berhasil disalin.", timer: 1600, showConfirmButton: false });
        } catch (e) {
          alert("Gagal menyalin teks.");
        }
      });
    });
  };

  const setupFilePreview = () => {
    const input = document.getElementById("bukti_transfer");
    const preview = document.getElementById("previewImage");
    const placeholder = document.getElementById("previewPlaceholder");
    if (!input || !preview || !placeholder) return;

    input.addEventListener("change", () => {
      const file = input.files && input.files[0];
      if (!file) {
        preview.classList.add("d-none");
        placeholder.classList.remove("d-none");
        preview.src = "";
        return;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        preview.src = e.target.result;
        preview.classList.remove("d-none");
        placeholder.classList.add("d-none");
      };
      reader.readAsDataURL(file);
    });
  };

  const setupPaymentImagePreview = () => {
    const input = document.getElementById("qris_image");
    const preview = document.getElementById("qrisPreview");
    const placeholder = document.getElementById("qrisPlaceholder");
    if (!input || !preview || !placeholder) return;

    input.addEventListener("change", () => {
      const file = input.files && input.files[0];
      if (!file) {
        if (preview.getAttribute("src")) {
          preview.classList.remove("d-none");
          placeholder.classList.add("d-none");
        } else {
          preview.classList.add("d-none");
          placeholder.classList.remove("d-none");
        }
        return;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        preview.src = e.target.result;
        preview.classList.remove("d-none");
        placeholder.classList.add("d-none");
      };
      reader.readAsDataURL(file);
    });
  };

  const setupSimulation = () => {
    const form = document.getElementById("simulasiForm");
    if (!form) return;
    const amount = document.getElementById("jumlah_pinjaman");
    const bunga = document.getElementById("bunga");
    const tenor = document.getElementById("tenor_minggu");
    const result = document.querySelector(".result-card");

    const renderLive = () => {
      if (!amount || !bunga || !tenor || !result) return;
      const a = parseFloat(amount.value || 0);
      const b = parseFloat(bunga.value || 0);
      const t = parseInt(tenor.value || 0, 10);
      if (a > 0 && t > 0 && b >= 0) {
        const totalBunga = a * (b / 100) * t;
        const totalTagihan = a + totalBunga;
        const angsuran = totalTagihan / t;
        const fmt = (n) => "Rp" + Math.round(n).toLocaleString("id-ID").replace(/,/g, ".");
        const box = result.querySelector(".summary-box h3");
        const box2 = result.querySelector(".summary-box.alt h3");
        if (box) box.textContent = fmt(totalTagihan);
        if (box2) box2.textContent = fmt(angsuran);
      }
    };

    [amount, bunga, tenor].forEach((el) => el && el.addEventListener("input", renderLive));
    renderLive();
  };

  const setupCharts = () => {
    if (!window.dashboardChartData || !document.getElementById("monthlyChart") || !window.Chart) return;
    const data = window.dashboardChartData;

    new Chart(document.getElementById("monthlyChart"), {
      type: "line",
      data: {
        labels: data.monthly_labels,
        datasets: [{
          label: "Pinjaman",
          data: data.monthly_values,
          tension: 0.35,
          fill: true,
          borderWidth: 2
        }]
      },
      options: { responsive: true, plugins: { legend: { display: false } } }
    });

    new Chart(document.getElementById("weeklyChart"), {
      type: "bar",
      data: {
        labels: data.weekly_labels,
        datasets: [{
          label: "Pembayaran",
          data: data.weekly_values,
          borderWidth: 0
        }]
      },
      options: { responsive: true, plugins: { legend: { display: false } } }
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    animateCounters();
    setupCopyButtons();
    setupFilePreview();
    setupPaymentImagePreview();
    setupSimulation();
    setupCharts();
  });
})();
