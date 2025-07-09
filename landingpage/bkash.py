url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create"

payload = {
    "mode": "0011",
    "callbackURL": "https://diabetestreeandtea.xyz/",
    "amount": "50",
    "currency": "BDT",
    "intent": "sale",
    "merchantInvoiceNumber": "#00112",
    "payerReference": "Ohy"
}
headers = {
    "accept": "application/json",
    "Authorization": "eyJraWQiOiJvTVJzNU9ZY0wrUnRXQ2o3ZEJtdlc5VDBEcytrckw5M1NzY0VqUzlERXVzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzZmNmMTFhOC0yYTI0LTQ5YjAtYjZlNC1iYTZkOGFiOWNlNDgiLCJhdWQiOiI2cDdhcWVzZmljZTAxazltNWdxZTJhMGlhaCIsImV2ZW50X2lkIjoiMGJkM2Y5YmUtYzI3OS00YTlkLWFjNjgtZjk0YWNjZjRlOGZlIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3Mzc3MTg2MDYsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMS5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMV9yYTNuUFkzSlMiLCJjb2duaXRvOnVzZXJuYW1lIjoiMDE3NzA2MTg1NjciLCJleHAiOjE3Mzc3MjIyMDYsImlhdCI6MTczNzcxODYwNn0.FxlLRCosDZTOiu9uV4M1C8g6Q1v78xtJe1Efo3WmYLvD0e-j_U0GFgWoTarx1be2ERzySg0EANJklUaIjI0o8T_SrTBSmZb5-Unl_ou4uctv2lJa8yw2UcpT9JrheE0u8zTC8A5lzkykD9JXV3O1q-D27a4pGM0vfuYRBOv8lUXfitZ7y129Y6r4wVzef0F-cLLxvOdWX9s6brZwdejPb8g3N1iHWIzz2rZYNy98ZN4vFhr9E4u_FbxQesYFYcsyO3KYxxxncXOWjlCmyahsCuz_h3cRpOPEnbhVRZAg4fBGVRZIZASUM_rz-hyYHxhoV-ZTSytpG8POt1xKK_KxOQ",
    "X-APP-Key": "0vWQuCRGiUX7EPVjQDr0EUAYtc",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)