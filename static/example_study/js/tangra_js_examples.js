

function do_tangra_request(url, success, failure, type, data)
{
	type = type || "GET";
	data = data || {};

	$.ajax(
				{
  					type:type,
  					url: url,
  					data: data,
  					success : success,
  					error : failure
				}
			);
}


function get_current_stage_success()
{
	$("#stage_number_div").html("YEAAAAHAHAHAH")
}


function get_current_stage_failure(data)
{
	$("#stage_number_div").html("booh" + data)
}


function get_current_stage()
{
	do_tangra_request(	"public_api/get_current_stage", 
						get_current_stage_success, 
						get_current_stage_failure
					 );
}




