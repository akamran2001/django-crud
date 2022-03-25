// Send a delete request when the delete button is clicked
const del = () => {
  let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  if (confirm("Are you sure you want to delete this")) {
    fetch(`${window.location}`, {
      method: "DELETE",
      headers: { "X-CSRFToken": csrftoken },
      mode: "same-origin",
    }).then((res) => {
      window.location.replace(res.url);
    });
  }
};
document.getElementById("delete").addEventListener("click", del);
