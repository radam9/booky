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

// event listener for edit and delete button
const edits = document.querySelectorAll(".edit");
const deletes = document.querySelectorAll(".delete");

for (let i = 0; i < edits.length; i++) {
  edits[i].addEventListener("click", (e) => {
    console.log("Edit Button Has been Clicked for ID: " + e.target.id + " !!!");
  });
}
for (let i = 0; i < deletes.length; i++) {
  deletes[i].addEventListener("click", (e) => {
    console.log(
      "Delete Button Has been Clicked for ID: " + e.target.id + " !!!"
    );
  });
}
