# https://n1290414.yclients.com/company/1177126/personal/select-time?o=m3570915s17612273d2425111900
def parse_url(url: str):
    company_id = url.split("company/")[1].split("/")[0]
    staff_id = url.split("personal/select-time?o=")[1].split("s")[0]

    return company_id, staff_id
