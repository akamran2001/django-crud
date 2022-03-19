// Send a delete request when the delete button is clicked
const del = () => {
  let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  fetch(`${window.location}`, {
    method: "POST",
    headers: { "X-CSRFToken": csrftoken },
    body: "DELETE",
    mode: "same-origin",
  }).then((res) => {
    window.location.replace(res.url);
  });
};
document.getElementById("delete").addEventListener("click", del);
