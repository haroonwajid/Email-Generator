from src.agent import email_agent
from src.utils import read_data, find_matching_domain_emails

def create_email():

    prospects, existing_customers = read_data("data/prospects.csv","data/customers.csv")

    mail_df = prospects.copy()


    # add a column to store the email content
    mail_df['Email Content'] = ""

    for index, row in prospects.iterrows():
        target_mail = row['Email']
        matching_orgs, flag = find_matching_domain_emails(target_mail, existing_customers)
        # remove nan values from existing customers
        matching_orgs = [org for org in matching_orgs if str(org) != 'nan']
        if flag:
            email = email_agent.invoke(f"{row['First Name']},{row['Last Name']}, {row['Email']}, {row['Title']}, {row['Company']} \n Existing customers with matching domain found: {', '.join(matching_orgs)}")
        else:
            email = email_agent.invoke(f"{row['First Name']},{row['Last Name']}, {row['Email']}, {row['Title']}, {row['Company']} \n No customers with matching domain found, here are two customers from our existing customers for reference: {', '.join(matching_orgs)}")
            
        print("Email sent to: ", target_mail)
        
        # append the email content to the mail_df
        mail_df.at[index, 'Email Content'] = email.content
        
    mail_df.to_csv("data/mail.csv", index=False)
    
        
    