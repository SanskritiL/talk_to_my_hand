const url = "process.php";
const form = document.querySelector("form");

function toSpanish() {
    var obj = { text: localStorage.getItem("letters") };
    fetch("http://localhost:8001/spanish_voice", {
      method: "post",
      body: JSON.stringify(obj)
    }).then(function(response) {
      console.log(response);
      response.json().then(data => {
        console.log("frm here ");
        console.log(data);

       
      });
    });



}

function toEnglish() {
    var obj = { text: localStorage.getItem("letters") };
    fetch("http://localhost:8001/english_voice", {
      method: "post",
      body: JSON.stringify(obj)
    }).then(function(response) {
      console.log(response);
      response.json().then(data => {
        console.log("frm here ");
        console.log(data);

       
      });
    });



}


form.addEventListener("submit", e => {
  e.preventDefault();

  const files = document.querySelector("[type=file]").files;
  const formData = new FormData();
  var result_text = "";
  var combo = "";

  for (let i = 0; i < files.length; i++) {
    let file = files[i];

    formData.append("files[]", file);
    console.log("from js");
    console.log(file);

    var obj = { image: file.name };
    fetch("http://localhost:8001/detect", {
      method: "post",
      body: JSON.stringify(obj)
    }).then(function(response) {
      console.log(response);
      response.json().then(data => {
        console.log("frm here ");
        console.log(data);
        result_text += data;

        localStorage.getItem("letters") == null
          ? localStorage.setItem("letters", "" + result_text)
          : localStorage.setItem(
              "letters",
              localStorage.getItem("letters") + result_text
            );
      });
    });
  }
  setTimeout(doSomething, 2000);

  function doSomething() {
    console.log("The localstorage is : " + localStorage.getItem("letters"));

    var myTag = document.getElementById("text-translate");
    console.log("resulting text is");
    var jsonString = localStorage.getItem("letters") + jsonString;
    console.log(jsonString);
    //console.log(combo);
    myTag.innerText = localStorage.getItem("letters");
  }

  //   console.log("outside")
  //   console.log(result_text);
  fetch(url, {
    method: "POST",
    body: formData
  }).then(response => {});
  document.getElementById("answer").style.visibility = "visible";
});
