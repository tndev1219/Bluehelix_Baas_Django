

def create_sign_msg(method,url, timestamp, body):
    params_list = [method, url, timestamp]
   
    if method == "POST":
        sorted_body = sorted(body.items(),  key=lambda d: d[0], reverse=False)
        print("sorted_body= ", sorted_body)

        data_list = []
        for data in sorted_body:
            if isinstance(data[1],list):
                value = "["+" ".join(data[1])+"]"
                key = data[0]
                data_list.append(key+"="+value)
            else:
                data_list.append("=".join(data))

        body_params = "&".join(data_list)
        params_list.append(body_params)

    params_str = "|".join(params_list)
    print("params_str= ", params_str)
    return params_str