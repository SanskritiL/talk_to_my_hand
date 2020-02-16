const url = "process.php";
const form = document.querySelector("form");

form.addEventListener("submit", e => {
  e.preventDefault();

  const files = document.querySelector("[type=file]").files;
  const formData = new FormData();
  var result_text = "";
  for (let i = 0; i < files.length; i++) {
    let file = files[i];

    formData.append("files[]", file);
    console.log("from js");
    console.log(file);

    var obj = { "image": file.name };
    fetch("http://localhost:8001/detect", {
      method: "post",
      body: JSON.stringify(obj)

    })
      .then(
          
        
        function(response) {
        console.log(response);
        response.json().then((data)=>{
            console.log("frm here ")
            console.log(data);
            result_text += data;
        });
        
      });
      
  }
  setTimeout(doSomething, 3000);

  function doSomething(){
    var myTag = document.getElementById("text-translate");
    myTag.innerText+= result_text
  }
  


  console.log("outside")
  console.log(result_text);
  fetch(url, {
    method: "POST",
    body: formData
  }).then(response => {});
  document.getElementById("answer").style.visibility = "visible";
});
