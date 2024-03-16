# DNS/DDNS A Record Updater
The purpose of this code is pretty simple, update the DNS A record for a given domain with the IP address of a DDNS record (or in theory the IP of any other DNS record).

## Getting Started
Should be pretty easy to use, first create a `.env` file (you can just copy the example file):

```sh
cp .env.example .env
```

You'll need to update the `.env` file with the appropriate API keys etc... Then to actually run the script (including creating a virtual environment, which is a best practice):

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python . <to_update_domain> <domain_to_get_ip_from>
```

Replacing `<to_update_domain>` and `<domain_to_get_ip_from>` respectively.

## Why
The rational behind why you might need/want this is a bit complicated. The basics are, if you have a registered domain then an A record is how that domain gets resolved to an IP.
Which means on some/enough DNS provides an A DNS record needs to be an IP. However, in some circumstances you may not have a static IP and so you may create a Dynamic DNS (DDNS) name, 
which largely functions exactly the same as a regular DNS name other than it usually has a shorter lifespans etc... and usually/can come with an update client to ensure that the name matches the proper IP.

Now, for specific reasons that won't be articulate here, keeping this DNS name and DDNS names separate was appealing. However, there was still a desire for the A record for the DNS name to point to the IP associated with the DDNS record such that if the IP changes the traffic still gets routed properly. That is where this comes in. It simply gets the 2 IPs checks them against each other and if DNS one needs to be updated, it updates it.

**Note**: This is currently only set up to work with GoDaddy because that's the only API for updating the record implemented. If people want to implement other provider APIs the structure of the project should make this easy by just extending the `DNSUpdater` (found in the `DNSUpdater.py` file in the `src` folder) class and updating the `__main__.py` (Admittedly, eventually might do some fancier import stuff stuff so this part isn't necessary but not there yet.)

## Setting up in cron
It's likely that you'd want to set this up as an automated task and one of the easiest ways to do this is to use cron

First, we need to edit the cron file
```sh
crontab -e
```

And then add the appropriate configurations (This specific line tells cron to run once a day at midnight)
```txt
0 0 * * * /path/to/folder/.venv/bin/python /path/to/folder/__main__.py <to_update_domain> <domain_to_get_ip_from>
```

Note, you'll have to replace `/path/to/folder`, `<to_update_domain>` and `<domain_to_get_ip_from>` appropriately.