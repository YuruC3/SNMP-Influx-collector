# IDRAC7/8

First under **IDRAC Settings** go to **Network**, and then to **Services**. There scroll down to **SNMP Agent** section and check the **Enabled** checkbox, set **SNMP Protocol** to **SNMP v3**. Under **SNMP Discovery Port Number** the SNMP port can be changed.

Thereafter under **IDRAC Settings** and **User Authentication** create a user. Do it by clicking a **User ID** number that does not have any user associated with it. Then click **Next** and check the **Enable User** checkbox, set a proper **User Name** for the user, set password under both **New Password** and **Confirm New Password**. After doing that, scroll down to **SNMP v3** section, check the **Enable SNMP v3** checkbox and select **SHA** under **Authentication type** and **AES** under **Privacy type**. 

Remember to click **Apply** at the end to save the user.

# IDRAC9

Hover over **IDRAC Settings** and click **Services**. There go to **SNMP Agent** and do the same thing as in IDRAC7 or IDRAC8. 

After enabling SNMP go to **Users** under **IDRAC Settings** and click **Local Users**. Click **Add** and fill the same fields as in IDRAC7 or IDRAC8. 