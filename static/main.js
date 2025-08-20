function setBusy(b){ b?$("#spinner").removeClass("d-none"):$("#spinner").addClass("d-none"); }
function renderRows(items){
  const $tb=$("#resultsTable tbody"); $tb.empty();
  items.forEach(x=>{
    $tb.append(`<tr>
      <td>${x.name}</td>
      <td>${x.condition}</td>
      <td class="text-center">${x.temp.toFixed(1)}</td>
      <td class="text-center">${x.humidity}</td>
    </tr>`);
  });
}
function renderStats(stats){
  if(!stats){ $("#statsBox").addClass("d-none"); return; }
  $("#statsText").html(`📊 <strong>Най-студен:</strong> ${stats.coldest_city} (${stats.coldest_temp.toFixed(1)} °C)
     &nbsp;|&nbsp; <strong>Средна:</strong> ${stats.avg_temp.toFixed(1)} °C`);
  $("#statsBox").removeClass("d-none");
}
$(function(){
  $("#btnRandom").on("click", function(){
    setBusy(true);
    $.getJSON("/api/random").done(d=>{
      renderRows(d.items||[]); renderStats(d.stats||null);
    }).fail(()=>alert("Грешка при зареждане")).always(()=>setBusy(false));
  });
  $("#btnCheck").on("click", function(){
    const q=$("#cityInput").val().trim(); if(!q){ alert("Въведи град (пример: London,GB)"); return; }
    setBusy(true);
    $.getJSON("/api/city",{q}).done(d=>{
      renderRows([d.item]); renderStats(null);
    }).fail((xhr)=>{
      alert((xhr.responseJSON && xhr.responseJSON.error) || "Грешка");
    }).always(()=>setBusy(false));
  });
});
