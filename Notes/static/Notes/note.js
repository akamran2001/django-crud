const del = () => {
  let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  fetch(`${window.location}`, {
    method: "DELETE",
    headers: { "X-CSRFToken": csrftoken },
    mode: "same-origin",
  }).then((res) => {
    window.location.replace(res.url);
  });
};
document.getElementById("delete").addEventListener("click", del);
