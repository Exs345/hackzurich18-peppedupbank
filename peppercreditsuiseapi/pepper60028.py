import http.client

conn = http.client.HTTPSConnection("csopenbankingzh.azurewebsites.net")

payload = "{ \n\t\n\t\"filter\" : [\t\n\t{\n\t\"attribute\" : \"kyc.job\" ,\n\t\"operator\" : \"like\" ,\n\t\"value\" : \"'%RETIRED%'\" \n\t},\n\t{\n\t\"attribute\" : \"id\" ,\n\t\"operator\" : \"like\" ,\n\t\"value\" : 600028 \n\t} \n\t] ,\n\t\n\t\"sorting\" : \" nickname asc\"\n\n}"

headers = {
    'content-type': "application/json",
    'accept': "application/json",
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik9UUXlRVGRCTkRFNU1rWTNNMFZFTnpNeU9EWkJOa1pETkRCR1FrRkZOamxDTTBJeE5EazRNdyJ9.eyJpc3MiOiJodHRwczovL2dicHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWI5Y2QwZTc3MmQ0YmI0N2Y5YTdjZmZlIiwiYXVkIjpbImh0dHBzOi8vb3BlbmJhbmtpbmcuY29tL2FwaSIsImh0dHBzOi8vZ2Jwcm9qZWN0LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1MzcwMDM4OTgsImV4cCI6MTUzNzA5MDI5OCwiYXpwIjoicThJTVlzMVNLekt0WExvdjhWM0pab3oxaE43MHgzQTciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZ3R5IjoicGFzc3dvcmQifQ.Ko7O6k5zVBgE7zjh4qREM82y8v-_Crz2QzR-m_-xgUk7e0-7vKceAuBZfEuMxW2Le5wx5oP3xI6h-SIEQ7Lnfzsy1N8gZijsSymjKl_u6N-qiUu3iC0NiRmnDauQ3a8blz6aPrJtWs_j7XnLnp5KPALSzhH-zpxg8XwmJaHIF18JNp3J1w0lupTN28nue1zAfIxWFLweS_Vl894CV5K4hQU08wx2YT7_4XO7TMqAxpx4o-eTn2qBtiDGq0lx7sEwwHgqqT2z6gTBiHy9Y4Zl7prUihPyIh3GvhERg-J7_T5HeFPmAxcqH_RboxBE_34H__bLjj8rKCsMZ31-iZ8Haw",
    'cache-control': "no-cache",
    'postman-token': "e7f6b6a6-852a-1425-908e-36b08de2db51"
    }

conn.request("POST", "/customers/search/unsecured", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))