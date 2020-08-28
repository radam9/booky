// event listener to change the orientation of the arrow beside folders when pressed
const sort = document.querySelectorAll(".folder-title,.subfolder-title");
for (let i = 0; i < sort.length; i++) {
  sort[i].addEventListener("click", (e) => {
    var element = e.target.children[0].classList;
    if (element.contains("fa-sort-down")) {
      element.replace("fa-sort-down", "fa-caret-right");
    } else {
      element.replace("fa-caret-right", "fa-sort-down");
    }
  });
}

// event listener for edit and delete button (modal window)
const modal = document.getElementById("modal");
const edits = document.querySelectorAll(".edit");
const deletes = document.querySelectorAll(".delete");

function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}

function toggleModal() {
  modal.classList.toggle("show-mymodal");
}
function removeModal() {
  toggleModal();
  modal.innerHTML = "";
}

for (let i = 0; i < edits.length; i++) {
  edits[i].addEventListener("click", (e) => {
    let id = e.target.id.slice(5);
    let link = "/modal_edit/" + id;
    fetch(link)
      .then(handleErrors)
      .then((response) => response.text())
      .then((data) => {
        modal.innerHTML += data;
        toggleModal();
        const cancel = modal.getElementsByClassName("btn-cancel")[0];
        const confirm = modal.getElementsByClassName("btn-confirm")[0];
        cancel.addEventListener("click", removeModal);
        confirm.addEventListener("click", () => {
          let title = modal.getElementsByClassName("mymodal-input-title")[0]
            .value;
          if (confirm.id == "Url") {
            let url = modal.getElementsByClassName("mymodal-input-url")[0]
              .value;
            var link = "/bookmarks/" + id + "/modify";
            var bookmark = { title: title, url: url };
          } else {
            var link = "/directories/" + id + "/modify";
            var bookmark = { title: title };
          }

          fetch(link, {
            method: "PATCH",
            credentials: "include",
            body: JSON.stringify(bookmark),
            cache: "no-cache",
            headers: new Headers({
              "content-type": "application/json",
            }),
          })
            .then(handleErrors)
            .then(() => {
              location.reload(true);
            });
        });
      })
      .catch((error) => {
        console.log(error);
      });
  });
}
for (let i = 0; i < deletes.length; i++) {
  deletes[i].addEventListener("click", (e) => {
    let id = e.target.id.slice(7);
    let link = "/modal_delete/" + id;
    fetch(link)
      .then(handleErrors)
      .then((response) => response.text())
      .then((data) => {
        modal.innerHTML += data;
        toggleModal();
        const close = modal.getElementsByClassName("btn-cancel")[0];
        const del = modal.getElementsByClassName("btn-confirm")[0];
        close.addEventListener("click", removeModal);
        del.addEventListener("click", () => {
          if (del.id == "Url") {
            var link = "/bookmarks/" + id + "/delete";
          } else {
            var link = "/directories/" + id + "/delete";
          }
          fetch(link, {
            method: "DELETE",
            credentials: "include",
            cache: "no-cache",
            headers: new Headers({
              "content-type": "application/json",
            }),
          })
            .then(handleErrors)
            .then(() => {
              location.reload(true);
            });
        });
      })
      .catch((error) => {
        console.log(error);
      });
  });
}
