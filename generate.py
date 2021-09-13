import random, json, re, uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def neo4j_format(a:dict):
    return re.sub(r'"([^"]+)":', r"\1:", json.dumps(a))

def random_name(n=None):
    first_names = "Amanda Amy Ashley Brittany Christopher Daniel David James Jason Jennifer Jessica John Joshua Kimberly Lisa Matthew Melissa Michael Michelle Robert Samantha".split()
    last_names = "Smith Johnson Williams Brown Jones Garcia Miller Davis Rodriguez".split()
    res = [f"{firstn} {lastn}" for lastn in last_names for firstn in first_names]
    random.shuffle(res)
    if n is not None:
        res = res[:n]
    return res

def random_borrower_detail():
    return {
        "AutomobilesOwnedCount": random.randint(0, 3),
        "BorrowerApplicationSignedDate": (datetime.today() - timedelta(
            days=random.randint(1, 365))).strftime("%Y-%m-%d"),
        "BorrowerBirthDate": (datetime.today() - relativedelta(
            years=random.randint(21, 80),
            days=random.randint(1, 365))).strftime("%Y-%m-%d"),
        "BorrowerClassificationType": random.sample(["Primary", "Secondary"], k=1)[0],
        "BorrowerMailToAddressSameAsPropertyIndicator": bool(random.randint(0, 1)),
        "BorrowerQualifyingIncomeAmount": random.randint(400, 10000),
        "BorrowerTotalMortgagedPropertiesCount": random.randint(0, 3),
        "CreditReportAuthorizationIndicator": bool(random.randint(0, 1)),
        "DependentCount": random.randint(0, 5),
        "DomesticRelationshipIndicator": bool(random.randint(0, 1)),
        "EmploymentStateType": random.sample(["Employed", "Unemployed"], k=1)[0],
        "IntentToProceedWithLoanTransactionIndicatedDate": (datetime.today() + timedelta(
            days=random.randint(1, 365))).strftime("%Y-%m-%d"),
        "SchoolingYearsCount": random.randint(5, 18)
    }

def random_address():
    number = random.randint(1, 3000)
    street = random.randint(1, 15)
    suffixes = ["st", "nd", "rd"]
    ordinal = (suffixes[street:] + ['th'])[0]
    cardinal_direction = random.sample(["N", "S", "W", "E"], k=1)[0]
    states = "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split()
    state = random.sample(states, k=1)[0]
    return f"{number} {street}{ordinal} Avenue {cardinal_direction}, {state}, USA"

def random_employer():
    types = ["Individual", "Legal Entity"]
    type_id = random.randint(0, 1)
    return {
        "name": random_name(1)[0] + ("'s Company" if type_id == 1 else ""),
        "type": types[type_id]
    }

def random_document():
    _id = str(uuid.uuid4())
    return {
        "name": f"Document {_id}",
        "type": "Employment"
    }

def main(borrowers=40, addresses=100, employers=20):
    # generating borrowers
    for name in random_name(borrowers):
        bd = random_borrower_detail()
        query = f'MERGE (b:Borrower {{name: "{name}"}})-[:HAS_DETAIL]->(bd:BorrowerDetail {neo4j_format(bd)});'
        print(query)
    # generating addresses
    for i in range(addresses):
        address = random_address()
        query = f'MERGE (a:Address {{name: "{address}"}});'
        print(query)
    # generating employers
    for i in range(employers):
        query = f'MERGE (e:Employer {neo4j_format(random_employer())})'
        if random.random() > 0.6:
            query += f'-[:HAS_DOCUMENT]->(d:Document {neo4j_format(random_document())})'
        print(query + ";")



if __name__ == "__main__":
    #test
    #print(random_name(3))
    #print(random_employer())
    #print(random_address())
    #print(random_document())
    #main(borrowers=0, addresses=0, employers=5)
    main()
    pass