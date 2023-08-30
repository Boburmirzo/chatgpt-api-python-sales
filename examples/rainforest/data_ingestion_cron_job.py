from rainforestapi_helper import send_request

params = {
  "category_id": "679255011"
  # ... any other params
}

data_dir = "./examples/rainforest"

send_request(data_dir, params)
