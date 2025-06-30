from flask import Blueprint, render_template
from app.forms.forms import IPCalculatorForm

bp = Blueprint('main', __name__)

def dtb(n):
    return format(n, '08b')

def cidr_to_subnet(CIDR):
    subnet = []
    for i in range(4):
        if CIDR >= 8:
            subnet.append(255)
            CIDR -= 8
        else:
            subnet.append(256 - 2**(8 - CIDR) if CIDR > 0 else 0)
            CIDR = 0
    return subnet

def determine_class(ip):
    first_octet = ip[0]
    if first_octet < 128:
        return 'A'
    elif first_octet < 192:
        return 'B'
    elif first_octet < 224:
        return 'C'
    elif first_octet < 240:
        return 'D (Multicast)'
    else:
        return 'E (Experimental)'

def is_private(ip):
    if ip[0] == 10:
        return True
    if ip[0] == 172 and 16 <= ip[1] <= 31:
        return True
    if ip[0] == 192 and ip[1] == 168:
        return True
    return False

@bp.route("/", methods=["GET", "POST"])
def index():
    form = IPCalculatorForm()
    result = None
    if form.validate_on_submit():
        ip_input = list(map(int, form.ip.data.split('.')))
        subnet_input = form.subnet.data

        if subnet_input.startswith('/'):
            CIDR = int(subnet_input[1:])
            subnet = cidr_to_subnet(CIDR)
        else:
            subnet = list(map(int, subnet_input.split('.')))
            CIDR = sum(dtb(octet).count('1') for octet in subnet)

        # Calculations
        network_id = [ip_input[i] & subnet[i] for i in range(4)]
        broadcast_address = [network_id[i] | (255 - subnet[i]) for i in range(4)]
        first_host = network_id.copy()
        first_host[3] += 1
        last_host = broadcast_address.copy()
        last_host[3] -= 1
        total_hosts = (2 ** (32 - CIDR)) - 2
        wildcard_mask = [255 - octet for octet in subnet]

        result = {
            "ip": '.'.join(map(str, ip_input)),
            "subnet_mask": '.'.join(map(str, subnet)),
            "cidr": f"/{CIDR}",
            "network_id": '.'.join(map(str, network_id)),
            "broadcast_address": '.'.join(map(str, broadcast_address)),
            "first_host": '.'.join(map(str, first_host)),
            "last_host": '.'.join(map(str, last_host)),
            "total_hosts": total_hosts,
            "ip_class": determine_class(ip_input),
            "is_private": "Private" if is_private(ip_input) else "Public",
            "ip_binary": '.'.join([dtb(b) for b in ip_input]),
            "subnet_binary": '.'.join([dtb(b) for b in subnet]),
            "network_binary": '.'.join([dtb(b) for b in network_id]),
            "wildcard_mask": '.'.join(map(str, wildcard_mask)),
            "total_subnets": 2 ** (CIDR - (8 * (CIDR // 8))) if CIDR % 8 != 0 else 1
        }

    return render_template("index.html", form=form, result=result)
