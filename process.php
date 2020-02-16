<?php 

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

	
    if (isset($_FILES['files'])) {
		$array_of_file = array();
        $errors = [];
        $path = 'uploads/';
	    $extensions = ['jpg', 'jpeg', 'png', 'gif'];
		
        $all_files = count($_FILES['files']['tmp_name']);

        for ($i = 0; $i < $all_files; $i++) {  
		$file_name = $_FILES['files']['name'][$i];
		$file_tmp = $_FILES['files']['tmp_name'][$i];
		$file_type = $_FILES['files']['type'][$i];
		$file_size = $_FILES['files']['size'][$i];
		$file_ext = strtolower(end(explode('.', $_FILES['files']['name'][$i])));

		$file = $path . $file_name;

		var_dump("the console looks like");
		//var_dump($file_name);
		array_push($array_of_file, $file_name);

		if (!in_array($file_ext, $extensions)) {
			$errors[] = 'Extension not allowed: ' . $file_name . ' ' . $file_type;
		}

		if ($file_size > 2097152) {
			$errors[] = 'File size exceeds limit: ' . $file_name . ' ' . $file_type;
		}

		if (empty($errors)) {
			move_uploaded_file($file_tmp, $file);
		}
	}
	var_dump($array_of_file);

	if ($errors) print_r($errors);
    }
}
?>
<script>
	var file_array = <?php echo json_encode($array_of_file); ?>;
	console.log("coming from script file")

// for(file in file_array){
// 	// filename_text = '{"text":"{hello}"}'
// 	var obj = {image: file};
// 	fetch('http://localhost:8001/detect', {
//     method: 'post',
//     body: JSON.stringify(obj)
//   }).then(function(response) {
// 	console.log(response);
// 	return response.json();
	
//   }).then(function(data) {
//     ChromeSamples.log('Created Gist:', data.html_url);
//   });
// }

	
</script>