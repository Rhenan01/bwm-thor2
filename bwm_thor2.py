import gc
import FreeSimpleGUI as sg
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import textwrap

from bwm import solve_bwm
from aggregation import aggregate_weights

sg.theme("PythonPlus")
sg.set_options(input_text_color='white', button_color=("white", "#0078D4"))

layout_initial = [
    [sg.Text("BWM THOR 2", justification='center', size=(35, 1), font=('Any', 20, 'bold'))],
    [sg.HorizontalSeparator()],
    [sg.Text("To name this software:")],
    [sg.Text("Tenório, Fabricio Maione; Santos, Rhenan Silva dos; Souza, Lucas Rocha de\n"
             "BWM THOR 2. 2025.", size=(35, 3), justification='center')],
    [sg.HorizontalSeparator()],
    [sg.Text("DECISION SUPPORT METHOD: BWM THOR 2", justification='center', size=(35, 1))],
    [sg.HorizontalSeparator()],
    [sg.Button("OK", key='-OK-')]
]
window_initial = sg.Window("Window Initial", layout_initial, element_justification='c', finalize=True, size=(350,225), grab_anywhere=True)
while True:
    event, values = window_initial.read()
    if event in (sg.WINDOW_CLOSED, '-OK-'):
        break
window_initial.close()

col1 = [
    [sg.Text("1º: Choose the number of alternatives, criteria and decision makers;")],
    [sg.Text("2º: Naming alternatives and criteria;")],
    [sg.Text("3º: Select the BEST and WORST criteria for each decision maker;")],
    [sg.Text("4º: Input preferences of the BEST criterion over the others;")],
    [sg.Text("5º: Input preferences of each criterion over the WORST;")],
    [sg.Text("6º: Calculate individual weights and consistency index ξ;")],
    [sg.Text("7º: Aggregate the weights of all decision makers;")],
]

col2 = [
    [sg.Text("8º: Input the p, q and discordance values for each criterion;")],
    [sg.Text("9º: Choose whether to use pertinences (If yes, fill in the pertinence matrix);")],
    [sg.Text("10º: Input the performance matrix of alternatives for each criterion;")],
    [sg.Text("11º: Display results of global evaluations;")],
    [sg.Text("12º: Choose whether to use RST and FRST modules;")],
    [sg.Text("13º: Display results of RST/FRST analysis;")],
    [sg.Text("14º: Choose if you want to run a new problem.")],
    [sg.Text("Let's start!")],
]

layout_instructions = [
    [sg.Text("Hello, the BWM THOR method will be executed in stages. They are:")],
    [sg.Column(col1, vertical_alignment='top'), sg.VerticalSeparator(), sg.Column(col2, vertical_alignment='top')],
    [sg.Button("OK")]
]
window_instructions = sg.Window("Instructions", layout_instructions, keep_on_top=True,
                                grab_anywhere=True)
while True:
    event_instructions, values_instructions = window_instructions.read()
    if event_instructions in (sg.WIN_CLOSED, "OK"):
        break
window_instructions.close()

control1 = 1
while control1 > 0:
    control1 = 0
    head1 = [[sg.Text("Number of alternatives:", size=(23, 0))] + [sg.Input(size=(3, 0), key="alt")]]
    head2 = [[sg.Text("Number of criteria:", size=(23, 0))] + [sg.Input(size=(3, 0), key="cri")]]
    head3 = [[sg.Text("Number of decision makers:", size=(23, 0))] + [sg.Input(size=(3, 0), key="num")]]
    layout = head1 + head2 + head3
    layout += [[sg.Button("Send data")]]
    window = sg.Window('Initial data', layout, font='Courier 12')
    event, values = window.Read()
    if event == sg.WIN_CLOSED:
        layout_popup = [[sg.Text("The program has been terminated, thank you for using BWM THOR2")]]
        window_popup = sg.Window('Good Bye', layout_popup)
        window_popup.read(timeout=1500)
        window_popup.close()
        sys.exit()
    window.close()
    cri = values["cri"]
    if not cri.isdigit():
        control1 += 1
    else:
        cri = int(cri)
    alt = values["alt"]
    if not alt.isdigit():
        control1 += 1
    else:
        alt = int(alt)
    num = values["num"]
    if not num.isdigit():
        control1 += 1
    else:
        num = int(num)
    if control1 > 0:
        sg.Popup("Error", "All values ​​must be numeric.")
weight = [];
weight2 = [];
weight3 = [];
weight4 = [];
ms1 = 0;
ms2 = 0;
ms3 = 0;
p = [];
q = [];
d = [];
t1 = [];
t2 = [];
t3 = [];
choice = 0;
keep = 0;
control = 0;
test = 0;
greatercontrol = 0;
dic = 0;
controller = 0
matrixs1 = [];
matrixs2 = [];
matrixs3 = [];
rs1 = [];
rs2 = [];
rs3 = [];
rs1o = [];
rs2o = [];
rs3o = [];
pertinence = [];
pertinence2 = [];
pertinencetca = [];
pertinence2tca = [];
index = [];
alternatives = [];
alternatives0 = [];
criteria = [];
cris1 = [];
cris2 = [];
cris3 = [];
cristotal = [];
var = 0;
meter = 0;
originals1 = [];
originals2 = [];
originals3 = [];
medtcan = [];
rtcan = [];
tcaneb = [];
neb = 0;
index = 0;
tca1 = 0;
tca2 = 0;
tca3 = 0;
f1 = 0;
f2 = 0;
f3 = 0;
ver1 = 0;
ver2 = 0;
ver3 = 0;
pos = 0;
weightF = [];
weightdec = [];
weightm = [1];
weightm2 = [1];
norm = 0;
ok = 0
for i in range(cri):
    weight.append(0)
for i in range(cri):
    weight2.append(0)
for i in range(cri):
    weight4.append(0)
headings = [[sg.Text("Name the alternatives:")]]
header = [[sg.Text('Alternative:')] + [sg.Input(size=(15, 1), pad=(0, 0)) for col in range(1)] for row in
          range(alt)]
layout = headings + header
layout += [[sg.Button("Send")]]
window = sg.Window('Alternative names', layout, font='Courier 12')
event, values = window.Read()
if event == sg.WIN_CLOSED:
    layout_popup = [[sg.Text("The program has been terminated, thank you for using BWM THOR2")]]
    window_popup = sg.Window('Good Bye', layout_popup)
    window_popup.read(timeout=1500)
    window_popup.close()
    sys.exit()
window.close()
for i in range(alt):
    alternatives.append(values[i])
headings = [[sg.Text("Name the criteria:")]]
header = [[sg.Text('Criteria:')] + [sg.Input(size=(15, 1), pad=(0, 0)) for col in range(1)] for row in range(cri)]
layout = headings + header
layout += [[sg.Button("Send")]]
window = sg.Window('Criteria names', layout, font='Courier 12')
event, values = window.Read()
if event == sg.WIN_CLOSED:
    layout_popup = [[sg.Text("The program has been terminated, thank you for using BWM THOR2")]]
    window_popup = sg.Window('Good Bye', layout_popup)
    window_popup.read(timeout=1500)
    window_popup.close()
    sys.exit()
window.close()
for i in range(cri):
    criteria.append(values[i])
for a in range(alt):
    row = []
    for b in range(alt):
        row.append(0)
    matrixs1.append(row)
for a in range(alt):
    row = []
    for b in range(alt):
        row.append(0)
    matrixs2.append(row)
for a in range(alt):
    row = []
    for b in range(alt):
        row.append(0)
    matrixs3.append(row)

def average(a):
    x = 0
    for i in range(len(a)):
        if (a[i]) != 0:
            x += a[i]
        tcam = (x / (len(a)))
    return tcam


def num_test(a):
    d = a.replace(".", "").replace(",", "")
    return d


def negative_test(a):
    d = a.replace("-", "")
    return d


def dotcomma(a):
    d = a.strip().replace(",", ".")
    return d


def discordances1(a, b, c):
    count1 = 0
    sum1 = 0
    Sumt = 0
    for i in range(cri):
        if not weight[i] == 0:
            if b[i] == "aPb":
                sum1 += weight[i] * c[i]
            elif b[i] == "aQb":
                Sumt += abs(weight[i] * c[i] * (((((abs(a[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5)))
            elif b[i] == "aIb":
                Sumt += weight[i] * 0.5 * c[i]
            elif b[i] == "bIa":
                Sumt += weight[i] * 0.5 * c[i]
                if abs(a[i]) >= d[i]:
                    count1 += 1
            elif b[i] == "bQa":
                Sumt += abs(weight[i] * c[i] * (((((abs(a[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5)))
                if abs(a[i]) >= d[i]:
                    count1 += 1
            elif b[i] == "bPa":
                Sumt += weight[i] * c[i]
                if abs(a[i]) >= d[i]:
                    count1 += 1
    global ms1
    if count1 > 0:
        ms1 = round(0.50, 3)
        return ms1
    else:
        ms1 = (sum1 / (Sumt + sum1))
        return ms1


def discordances2(a, b, c):
    cont2 = 0
    sum1 = 0
    Sumt = 0
    for i in range(cri):
        if not weight[i] == 0:
            if b[i] == "aPb":
                sum1 += weight[i] * c[i]
            elif b[i] == "aQb":
                sum1 += abs(weight[i] * c[i] * (((((abs(a[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5)))
            elif b[i] == "aIb":
                Sumt += weight[i] * 0.5 * c[i]
            elif b[i] == "bIa":
                Sumt += weight[i] * 0.5 * c[i]
                if abs(a[i]) >= d[i]:
                    cont2 += 1
            elif b[i] == "bQa":
                Sumt += abs(weight[i] * c[i] * (((((abs(a[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5)))
                if abs(a[i]) >= d[i]:
                    cont2 += 1
            elif b[i] == "bPa":
                Sumt += weight[i] * c[i]
                if abs(a[i]) >= d[i]:
                    cont2 += 1
    global ms2
    if cont2 > 0:
        ms2 = round(0.50, 3)
        return ms2
    else:
        ms2 = (sum1 / (Sumt + sum1))
        return ms2


def discordances3(a, b, c):
    cont3 = 0
    sum1 = 0
    Sumt = 0
    for i in range(cri):
        if not weight[i] == 0:
            if b[i] == "aPb":
                sum1 += weight[i] * c[i]
            elif b[i] == "aQb":
                sum1 += abs(weight[i] * c[i] * (((((abs(a[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5)))
            elif b[i] == "aIb":
                sum1 += weight[i] * 0.5 * c[i]
            elif b[i] == "bIa":
                sum1 += weight[i] * 0.5 * c[i]
                if abs(a[i]) >= d[i]:
                    cont3 += 1
            elif b[i] == "bQa":
                Sumt += abs(weight[i] * c[i] * ((((abs(a[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5))
                if abs(a[i]) >= d[i]:
                    cont3 += 1
            elif b[i] == "bPa":
                Sumt += weight[i] * c[i]
                if abs(a[i]) >= d[i]:
                    cont3 += 1
    global ms3
    if cont3 > 0:
        ms3 = round(0.50, 3)
        return ms3
    else:
        ms3 = (sum1 / (Sumt + sum1))
        return ms3


def s1(a, b, c):
    sum11 = 0
    sum21 = 0
    for i in range(cri):
        if a[i] == "aPb":
            sum11 += weight[i] * c[i]
        elif a[i] == "aQb":
            sum21 += abs((weight[i]) * (c[i]) * (((((abs(b[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5)))
        elif a[i] == "aIb":
            sum21 += weight[i] * 0.5 * c[i]
        elif a[i] == "bIa":
            sum21 += weight[i] * 0.5 * c[i]
        elif a[i] == "bQa":
            sum21 += abs((weight[i]) * (c[i]) * (((((abs(b[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5)))
        elif a[i] == "bPa":
            sum21 += weight[i] * c[i]
    if (sum11 > sum21):
        return "dominates"
    else:
        return "does not dominate"


def s2(a, b, c):
    sum12 = 0
    sum22 = 0
    for i in range(cri):
        if a[i] == "aPb":
            sum12 += weight[i] * c[i]
        elif a[i] == "aQb":
            sum12 += abs(weight[i] * c[i] * (((((abs(b[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5)))
        elif a[i] == "aIb":
            sum22 += weight[i] * 0.5 * c[i]
        elif a[i] == "bIa":
            sum22 += weight[i] * 0.5 * c[i]
        elif a[i] == "bQa":
            sum22 += abs(weight[i] * c[i] * (((((abs(b[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5)))
        elif a[i] == "bPa":
            sum22 += weight[i] * c[i]
    if (sum12 > sum22):
        return "dominates"
    else:
        return "does not dominate"


def s3(a, b, c):
    sum13 = 0
    sum23 = 0
    for i in range(cri):
        if a[i] == "aPb":
            sum13 += weight[i] * c[i]
        elif a[i] == "aQb":
            sum13 += abs(weight[i] * c[i] * (((((abs(b[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5)))
        elif a[i] == "aIb":
            sum13 += weight[i] * 0.5 * c[i]
        elif a[i] == "bIa":
            sum13 += weight[i] * 0.5 * c[i]
        elif a[i] == "bQa":
            sum23 += abs(weight[i] * c[i] * (((((abs(b[i])) - q[i]) / (p[i] - q[i])) * (0.5) + 0.5)))
        elif a[i] == "bPa":
            sum23 += weight[i] * c[i]
    if (sum13 > sum23):
        return "dominates"
    else:
        return "does not dominate"


def ind(a, b, c):
    x = float((a + b + c) / 3)
    return x


def dif(a, b):
    x = a - b
    return x

# Data coming from the beginning of the code
n = cri
d = num
all_weights = []

for decisor in range(1, d + 1):
    sg.popup(f"🔎 Starting input for Decision Maker #{decisor}", title="Group BWM")
    combo_width = max(len(c) for c in criteria) + 5
    window_layout_BW_criteria = [
        [sg.Text('Select the BEST criterion:', size=(25, 1)), sg.Combo(criteria, key='best', readonly=True, size=(combo_width, 1))],
        [sg.Text('Select the WORST criterion:', size=(25, 1)), sg.Combo(criteria, key='worst', readonly=True, size=(combo_width, 1))],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]

    window_BW_criteria = sg.Window(
        'Best and Worst Criteria Selection',
        window_layout_BW_criteria,
        finalize=True,
        location=(None, None)
    )

    while True:
        event_window_BW_criteria, values_window_BW_criteria = window_BW_criteria.read()

        if event_window_BW_criteria in (sg.WIN_CLOSED, 'Cancel'):
            layout_popup = [[sg.Text("The program has been terminated. Thank you for using BWM THOR2.")]]
            window_popup = sg.Window('Goodbye', layout_popup)
            window_popup.read(timeout=1500)
            window_popup.close()
            sys.exit()

        if event_window_BW_criteria == 'Submit':
            best = values_window_BW_criteria['best']
            worst = values_window_BW_criteria['worst']

            if not best or not worst:
                sg.popup('⚠️ Please select both criteria before continuing.')
            elif best == worst:
                sg.popup('❌ The BEST and WORST criteria must be different.')
            else:
                sg.popup(f'✅ Valid criteria selected:\n\n'
                         f'{"Best criterion:":<18} {best}\n'
                         f'{"Worst criterion:":<18} {worst}',
                         title='Criteria Confirmed')
                window_BW_criteria.close()
                break

    scale_values = [str(i) for i in range(1, 10)]  # escala de 1 a 9 como strings

    bo_inputs = []
    ow_inputs = []
    layout_bo = [[sg.Text(f'How much is BEST ({best}) preferred over each criterion?')]]
    layout_ow = [[sg.Text(f'How much is each criterion preferred over WORST ({worst})?')]]
    best_index = criteria.index(best)
    worst_index = criteria.index(worst)
    for i, crit in enumerate(criteria):
        if i == best_index:
            layout_bo.append([sg.Text(f'{best} vs {crit}: 1 (fixed)')])
            bo_inputs.append(1.0)
        else:
            key = f'bo_{i}'
            layout_bo.append([
                sg.Text(f'{best} vs {crit}:'),
                sg.Combo(scale_values, key=key, readonly=True, size=(5, 1))
            ])
            bo_inputs.append(key)

    for i, crit in enumerate(criteria):
        if i == worst_index:
            layout_ow.append([sg.Text(f'{crit} vs {worst}: 1 (fixed)')])
            ow_inputs.append(1.0)
        else:
            key = f'ow_{i}'
            layout_ow.append([
                sg.Text(f'{crit} vs {worst}:'),
                sg.Combo(scale_values, key=key, readonly=True, size=(5, 1))
            ])
            ow_inputs.append(key)

    layout_BO_OW = layout_bo + [[sg.HorizontalSeparator()]] + layout_ow + [[sg.Button('Submit'), sg.Button('Cancel')]]
    window_BO_OW = sg.Window('Pairwise Comparisons', layout_BO_OW, finalize=True)


    while True:
        event_window_BO_OW, values_window_BO_OW = window_BO_OW.read()

        if event_window_BO_OW in (sg.WIN_CLOSED, 'Cancel'):
            layout_popup = [[sg.Text("The program has been terminated. Thank you for using BWM THOR2.")]]
            window_popup = sg.Window('Goodbye', layout_popup)
            window_popup.read(timeout=1500)
            window_popup.close()
            sys.exit()

        if event_window_BO_OW == 'Submit':
            try:
                final_bo = []
                for v in bo_inputs:
                    if isinstance(v, str):
                        val = int(values_window_BO_OW[v])
                        final_bo.append(val)
                    else:
                        final_bo.append(v)

                final_ow = []
                for v in ow_inputs:
                    if isinstance(v, str):
                        val = int(values_window_BO_OW[v])
                        final_ow.append(val)
                    else:
                        final_ow.append(v)

                # Show results
                bo_str = "\n".join([f"{best} vs {criteria[i]}: {val}" for i, val in enumerate(final_bo)])
                ow_str = "\n".join([f"{criteria[i]} vs {worst}: {val}" for i, val in enumerate(final_ow)])
                sg.popup_scrolled(f"✅ BO vector:\n{bo_str}\n\n✅ OW vector:\n{ow_str}",
                                  title='Vectors Confirmed')

                window_BO_OW.close()
                break

            except:
                sg.popup('❌ Please select a value from 1 to 9 for each comparison.')

    try:
        weights, xi = solve_bwm(best_index, worst_index, final_bo, final_ow)

        weight_str = "\n".join([f"{criteria[i]}: {weights[i]:.4f}" for i in range(len(criteria))])
        sg.popup_scrolled(f"📊 Final Weights:\n{weight_str}\n\n"
                          f"📉 Consistency index ξ: {xi:.4f}",
                          title="BWM Results")
        all_weights.append(list(weights))
    except Exception as e:
        sg.popup_error(f"❌ Error solving BWM for DM#{decisor}:\n{e}")
        sys.exit()
        
geom_means = aggregate_weights(all_weights)

weight_str = "\n".join(
    [
        f"{criteria[i]}: {geom_means[i]:.4f}"
        for i in range(len(criteria))
    ]
)

sg.popup_scrolled(
    f"📊 Aggregated Final Weights (Geometric Mean):\n{weight_str}",
    title="Group BWM Result",
)

def_weights = geom_means

while test != "error":
    control = 0;
    greatercontrol = 0;
    control1 = 0
    headings = criteria
    def wrap_text(text, width):
        return '\n'.join(textwrap.wrap(text, width))
    max_line_width = 20
    wrapped_headers = [wrap_text(h, max_line_width) for h in criteria]
    header = [
        [sg.Text(' ')] + [
            sg.Text(h, size=(max_line_width, None), pad=(0, (5, 0)), justification='center', auto_size_text=True)
            for h in wrapped_headers
        ]
    ]
    h1 = [[sg.Text("p ", pad=((5, 0), (0, 10)))] + [
        sg.Input(size=(max_line_width, 1), pad=(0, 0), justification='center') for _ in criteria
    ]]
    h2 = [[sg.Text("q ", pad=((5, 0), (0, 10)))] + [
        sg.Input(size=(max_line_width, 1), pad=(0, 0), justification='center') for _ in criteria
    ]]
    layout = header + h1 + h2 + [[sg.Button("Send")]]
    window = sg.Window('p and q values', layout, font='Courier 12')
    event, values = window.Read()
    if event == sg.WIN_CLOSED:
        layout_popup = [[sg.Text("The program has been terminated, thank you for using BWM THOR2")]]
        window_popup = sg.Window('Good Bye', layout_popup)
        window_popup.read(timeout=1500)
        window_popup.close()
        sys.exit()
    window.close()
    for j in range(2 * cri):
        if not values[j].isdigit():
            control1 += 1
            controller = num_test(values[j])
            if controller.isdigit():
                control1 -= 1
            else:
                controller = negative_test(controller)
                if controller.isdigit():
                    control1 -= 1
    if control1 == 0:
        for j in range(2 * cri):
            if float(dotcomma(values[j])) < 0:
                control += 1
        for j in range(cri):
            if float(dotcomma(values[j])) <= float(dotcomma(values[j + cri])):
                greatercontrol += 1
        if control > 0 and greatercontrol > 0:
            sg.Popup("The values ​​of p and q must be greater than or equal to 0 and the value of p must be greater than q.")
        elif control > 0:
            sg.Popup("The values ​​of p and q must be greater than or equal to 0")
        elif greatercontrol > 0:
            sg.Popup("The value of p must be greater than q.")
        else:
            test = "error"
    else:
        sg.Popup("error", "Values ​​must be numeric.")
p = []
for j in range(cri):
    p.append(float(dotcomma(values[j])))
q = []
for j in range(cri):
    q.append(float(dotcomma(values[cri + j])))
control1 = 1
while control1 > 0:
    control1 = 0
    headings = criteria
    max_line_width = 20
    wrapped_headers = [wrap_text(h, max_line_width) for h in criteria]
    header = [
        [sg.Text('           ')] + [
            sg.Text(h, size=(max_line_width, None), pad=(0, (5, 0)), justification='center', auto_size_text=True)
            for h in wrapped_headers
        ]
    ]
    h3 = [[sg.Text("discordance ", pad=((5, 0), (0, 10)))] + [
        sg.Input(size=(max_line_width, 1), pad=(0, 0), justification='center') for _ in criteria
    ]]
    layout = header + h3 + [[sg.Button("Send")]]
    window = sg.Window('Discordance matrix', layout, font='Courier 12', resizable=True, finalize=True)
    for i in range(len(criteria)):
        window[h3[0][1 + i].Key].expand(expand_x=True)
    event, values = window.Read()
    if event == sg.WIN_CLOSED:
        layout_popup = [[sg.Text("The program has been terminated, thank you for using BWM THOR2")]]
        window_popup = sg.Window('Good Bye', layout_popup)
        window_popup.read(timeout=1500)
        window_popup.close()
        sys.exit()
    window.close()
    for i in range(cri):
        if not values[i].isdigit():
            control1 += 1
            controller = num_test(values[i])
            if controller.isdigit():
                control1 -= 1
            else:
                controller = negative_test(controller)
                if controller.isdigit():
                    control1 -= 1
    if control1 > 0:
        sg.Popup("error", "Values ​​must be numeric.")
d = []
for i in range(cri):
    d.append(float(dotcomma(values[i])))
# Pertinences
head = [[sg.Text("Do you want to use pertinence?", size=(26, 0))]]
radio = [[sg.Radio("Yes", "continue", key="yes3")] + [sg.Radio("No", "continue", key="no3")]]
layout = head + radio
layout += [[sg.Button("Send data")]]
window = sg.Window('Pertinence', layout, font='Courier 12')
event, values = window.Read()
if event == sg.WIN_CLOSED:
    layout_popup = [[sg.Text("The program has been terminated, thank you for using BWM THOR2")]]
    window_popup = sg.Window('Good Bye', layout_popup)
    window_popup.read(timeout=1500)
    window_popup.close()
    sys.exit()
window.close()
yes3 = values["yes3"]
no3 = values["no3"]
if yes3 == True:
    usepert = 0
elif no3 == True:
    usepert = 1
if usepert == 0:
    test = 0;
    control = 0
    pertinence = []
    pertinencetca = []
    for i in range(cri):
        pertinence.append(1)
        pertinencetca.append(1)
else:
    for i in range(cri):
        pertinence.append(1)
        pertinencetca.append(1)
matrix = []
matrix = []
for a in range(alt):
    row = []
    for b in range(cri):
        row.append(0)
    matrix.append(row)
for a in range(alt):
    row = []
    for b in range(cri):
        row.append(0)
    pertinence2.append(row)
for a in range(alt):
    row = []
    for b in range(cri):
        row.append(0)
    pertinence2tca.append(row)

if usepert == 0:
    control = 0;
    test = 0;
    dic = 0
    while test != "error":
        control = 0;
        control1 = 0
        headings = criteria
        max_line_width = 20
        wrapped_headers = [wrap_text(h, max_line_width) for h in criteria]
        header = [
            [sg.Text('              ')] + [
                sg.Text(h, size=(max_line_width, None), pad=(0, (5, 0)), justification='center',
                        auto_size_text=True) for h in wrapped_headers
            ]
        ]
        layout_alternatives = []
        for i in range(alt):
            h = [[sg.Text(f"{alternatives[i]}", pad=((0, 0), (0, 10)), size=(15, 1), justification='center')] + [
                sg.Input(size=(max_line_width, 1), pad=(0, 0), justification="center") for _ in criteria
            ]]
            layout_alternatives += h
        layout = header + layout_alternatives + [[sg.Button("Send")]]
        window = sg.Window('Pertinence matrix', layout, font='Courier 12', resizable=True, finalize=True)
        for i in range(len(criteria)):
            window[layout_alternatives[0][1 + i].Key].expand(expand_x=True)
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            layout_popup = [[sg.Text("The program has been terminated, thank you for using BWM THOR2")]]
            window_popup = sg.Window('Good Bye', layout_popup)
            window_popup.read(timeout=1500)
            window_popup.close()
            sys.exit()
        window.close()
        for i in range(alt * cri):
            if not values[i].isdigit():
                control1 += 1
                controller = num_test(values[i])
                if controller.isdigit():
                    control1 -= 1
                else:
                    controller = negative_test(controller)
                    if controller.isdigit():
                        control1 -= 1
        if control1 == 0:
            for i in range(alt * cri):
                if float(dotcomma(values[i])) > 1 or float(dotcomma(values[i])) < 0:
                    control += 1
            if control > 0:
                sg.Popup("The pertinence value must be between 0 and 1.")
            else:
                test = "error"
        else:
            sg.Popup("error", "Values ​​must be numeric.")
    for i in range(alt):
        for j in range(cri):
            pertinence2[i][j] = float(dotcomma(values[dic]))
            pertinence2tca[i][j] = float(dotcomma(values[dic]))
            dic += 1
else:
    for i in range(alt):
        for j in range(cri):
            pertinence2[i][j] = 1
            pertinence2tca[i][j] = 1
control1 = 1
while control1 > 0:
    control1 = 0
    dic = 0
    headings = criteria
    max_line_width = 20
    wrapped_headers = [wrap_text(h, max_line_width) for h in criteria]
    header = [
        [sg.Text('              ')] + [
            sg.Text(h, size=(max_line_width, None), pad=(0, (5, 0)), justification='center',
                    auto_size_text=True) for h in wrapped_headers
        ]
    ]
    layout_alternatives = []
    for i in range(alt):
        h = [[sg.Text(f"{alternatives[i]}", pad=((0, 0), (0, 10)), size=(15, 1), justification='center')] + [
            sg.Input(size=(max_line_width, 1), pad=(0, 0), justification="center") for _ in criteria
        ]]
        layout_alternatives += h
    layout = header + layout_alternatives + [[sg.Button("Send")]]
    window = sg.Window('Matrix of alternatives', layout, font='Courier 12', resizable=True, finalize=True)
    for i in range(len(criteria)):
        window[layout_alternatives[0][1 + i].Key].expand(expand_x=True)
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        layout_popup = [[sg.Text("The program has been terminated, thank you for using BWM THOR2")]]
        window_popup = sg.Window('Good Bye', layout_popup)
        window_popup.read(timeout=1500)
        window_popup.close()
        sys.exit()
    window.close()
    for i in range(alt * cri):
        if not values[i].isdigit():
            control1 += 1
            controller = num_test(values[i])
            if controller.isdigit():
                control1 -= 1
            else:
                controller = negative_test(controller)
                if controller.isdigit():
                    control1 -= 1
    if control1 == 0:
        for i in range(alt):
            for j in range(cri):
                matrix[i][j] = float(dotcomma(values[dic]))
                dic += 1
    else:
        sg.Popup("error", "Values ​​must be numeric.")


weight = def_weights
rounded_weight = np.round(weight, 3)
sg.Popup("The resulting weight matrix was:", rounded_weight)
test = []
dic = 0
for i in range(cri):
    weight2[i] = weight[i]
    weight4[i] = weight[i]
def compare(a, b):
    if (a - b) > p[k]:
        x = "aPb"
    elif (a - b) > q[k]:
        x = "aQb"
    elif (a - b) >= 0:
        x = "aIb"
    elif (a - b) >= (-q[k]):
        x = "bIa"
    elif (a - b) >= (-p[k]):
        x = "bQa"
    elif (a - b) < (-p[k]):
        x = "bPa"
    return x


average1 = round(average(pertinence), 4)
medtcan.append(average1)
for i in range(alt):
    average1 = round(average(pertinence2[i]), 4)
    medtcan.append(average1)
for i in range(1, alt + 1):
    average1 = round(((medtcan[0] + medtcan[i]) / 2), 4)
    medtcan.append(average1)
# S1
c = [];
b = [];
e = [];
f = [];
g = [];
h = [];
lower = max(weight)
meter = 0
while meter < 1:
    c = [];
    b = [];
    e = [];
    f = [];
    g = [];
    h = [];
    x = 0;
    y = 0;
    w = 0;
    z = 0;
    v = 0;
    t = 0;
    rs1 = [];
    rs1o = []
    if meter != 0:
        lower = max(weight2)
        for j in range(cri):
            if weight2[j] < lower and weight2.index(lower) not in weight3 and weight2[j] > 0:
                lower = weight2[j]
        weight3.append(weight2.index(lower))
        weight2[weight2.index(lower)] = 0
        weight[weight3[meter - 1]] = 0
    for i in range(alt):
        for j in range(alt):
            if (i < j):
                for k in range(cri):
                    x = compare(matrix[i][k], matrix[j][k])
                    y = dif(matrix[i][k], matrix[j][k])
                    w = compare(matrix[j][k], matrix[i][k])
                    z = dif(matrix[j][k], matrix[i][k])
                    v = ind(pertinence[k], pertinence2[i][k], pertinence2[j][k])
                    t = ind(pertinence[k], pertinence2[j][k], pertinence2[i][k])
                    b.append(y)
                    c.append(x)
                    e.append(w)
                    f.append(z)
                    g.append(v)
                    h.append(t)
                if (s1(c, b, g) == "dominates") and (s1(e, f, h) == "dominates"):
                    if (discordances1(b, c, g) == 0.5) or (discordances1(f, e, h) == 0.5):
                        matrixs1[i][j] = 0.5
                        matrixs1[j][i] = 0.5
                    else:
                        matrixs1[i][j] = round(discordances1(b, c, g), 3)
                        matrixs1[j][i] = round(discordances1(f, e, h), 3)
                elif (s1(c, b, g) == "dominates") and (s1(e, f, h) != "dominates"):
                    if (discordances1(b, c, g) != 0.5):
                        matrixs1[i][j] = round(ms1, 3)
                        matrixs1[j][i] = 0
                    else:
                        matrixs1[i][j] = 0.5
                        matrixs1[j][i] = 0.5
                elif (s1(c, b, g) != "dominates") and (s1(e, f, h) == "dominates"):
                    if (discordances1(f, e, h) != 0.5):
                        matrixs1[i][j] = 0
                        matrixs1[j][i] = round(ms1, 3)
                    else:
                        matrixs1[i][j] = 0.5
                        matrixs1[j][i] = matrixs1[i][j]
                else:
                    matrixs1[i][j] = 0.5
                    matrixs1[j][i] = matrixs1[i][j]
                c = [];
                b = [];
                e = [];
                f = [];
                g = [];
                h = []
    for i in range(alt):
        r1 = 0.0
        for j in range(alt):
            r1 += matrixs1[i][j]
        rs1.append(round(r1, 3))
    for i in range(len(rs1)):
        rs1o.append(rs1[i])
    rs1o.sort()
    rs1o.reverse()
    for i in range(alt):
        for j in range(alt):
            if rs1o[i] == rs1[j]:
                if alternatives[j] in alternatives0:
                    "nothing"
                else:
                    alternatives0.append(alternatives[j])
    for i in range(alt):
        if (i != alt - 1):
            if rs1o[i] > rs1o[i + 1]:
                alternatives0.insert(2 * i + 1, ">")
                if meter == 0:
                    originals1.append(alternatives0[2 * i])
                    originals1.append(">")
            elif rs1o[i] == rs1o[i + 1]:
                alternatives0.insert(2 * i + 1, "=")
                if meter == 0:
                    originals1.append(alternatives0[2 * i])
                    originals1.append("=")
        else:
            if meter == 0:
                originals1.append(alternatives0[2 * i])
    if meter == 0:
        header = [[sg.Text('S1', justification='center', size=(35, 1), font=('Any', 20, 'bold'))]]
        input_rows = [
            [sg.Text(alternatives[row])] + [sg.Text("-")] + [sg.Text(matrixs1[row][col]) for col in range(alt)] for
            row in range(alt)]
        jump = [[sg.Text("")]]
        Summat = [[sg.Text("Summation:")]]
        bottom = [[sg.Text(alternatives[row])] + [sg.Text("=")] + [sg.Text(rs1[row]) for col in range(1)] for row
                  in range(alt)]
        jump2 = [[sg.Text("")]]
        order = [[sg.Text(alternatives0[col]) for col in range(len(alternatives0))] + [sg.Text("- Original")] for
                 row in range(1)]
        layout = header + input_rows + jump + Summat + bottom + jump2 + order
        layout += [[sg.Button("Send")]]
        window = sg.Window('Results of S1', layout, font='Courier 12')
        event, values = window.Read()
        window.close()
    alternatives0 = []
    tca1 = 0
    ver1 = 0
    meter += 1
meter = 0;
weight3 = []
for i in range(cri):
    weight[i] = weight4[i]
    weight2[i] = weight4[i]
# S2
while meter < 1:
    c = [];
    b = [];
    e = [];
    f = [];
    g = [];
    h = [];
    x = 0;
    y = 0;
    w = 0;
    z = 0;
    v = 0;
    t = 0;
    rs2 = [];
    rs2o = []
    if meter != 0:
        lower = max(weight2)
        for j in range(cri):
            if weight2[j] < lower and weight2.index(lower) not in weight3 and weight2[j] > 0:
                lower = weight2[j]
        weight3.append(weight2.index(lower))
        weight2[weight2.index(lower)] = 0
        weight[weight3[meter - 1]] = 0
    for i in range(alt):
        for j in range(alt):
            if (i < j):
                for k in range(cri):
                    x = compare(matrix[i][k], matrix[j][k])
                    y = dif(matrix[i][k], matrix[j][k])
                    w = compare(matrix[j][k], matrix[i][k])
                    z = dif(matrix[j][k], matrix[i][k])
                    v = ind(pertinence[k], pertinence2[i][k], pertinence2[j][k])
                    t = ind(pertinence[k], pertinence2[j][k], pertinence2[i][k])
                    b.append(y)
                    c.append(x)
                    e.append(w)
                    f.append(z)
                    g.append(v)
                    h.append(t)
                if (s2(c, b, g) == "dominates") and (s2(e, f, h) == "dominates"):
                    if (discordances2(b, c, g) == 0.5) or (discordances2(f, e, h) == 0.5):
                        matrixs2[i][j] = 0.5
                        matrixs2[j][i] = 0.5
                    else:
                        matrixs2[i][j] = round(discordances2(b, c, g), 3)
                        matrixs2[j][i] = round(discordances2(f, e, h), 3)
                elif (s2(c, b, g) == "dominates") and (s2(e, f, h) != "dominates"):
                    if (discordances2(b, c, g) != 0.5):
                        matrixs2[i][j] = round(ms2, 3)
                        matrixs2[j][i] = 0
                    else:
                        matrixs2[i][j] = 0.5
                        matrixs2[j][i] = 0.5
                elif (s2(c, b, g) != "dominates") and (s2(e, f, h) == "dominates"):
                    if (discordances2(f, e, h) != 0.5):
                        matrixs2[i][j] = 0
                        matrixs2[j][i] = round(ms2, 3)
                    else:
                        matrixs2[i][j] = 0.5
                        matrixs2[j][i] = matrixs2[i][j]
                else:
                    matrixs2[i][j] = 0.5
                    matrixs2[j][i] = matrixs2[i][j]
                c = [];
                b = [];
                e = [];
                f = [];
                g = [];
                h = []
    for i in range(alt):
        r2 = 0.0
        for j in range(alt):
            r2 += matrixs2[i][j]
        rs2.append(round(r2, 3))
    for i in range(len(rs2)):
        rs2o.append(rs2[i])
    rs2o.sort()
    rs2o.reverse()
    for i in range(alt):
        for j in range(alt):
            if rs2o[i] == rs2[j]:
                if alternatives[j] in alternatives0:
                    "nothing"
                else:
                    alternatives0.append(alternatives[j])
    for i in range(alt):
        if (i != alt - 1):
            if rs2o[i] > rs2o[i + 1]:
                alternatives0.insert(2 * i + 1, ">")
                if meter == 0:
                    originals2.append(alternatives0[2 * i])
                    originals2.append(">")
            elif rs2o[i] == rs2o[i + 1]:
                alternatives0.insert(2 * i + 1, "=")
                if meter == 0:
                    originals2.append(alternatives0[2 * i])
                    originals2.append("=")
        else:
            if meter == 0:
                originals2.append(alternatives0[2 * i])
    if meter == 0:
        header = [[sg.Text('S2', justification='center', size=(35, 1), font=('Any', 20, 'bold'))]]
        input_rows = [
            [sg.Text(alternatives[row])] + [sg.Text("-")] + [sg.Text(matrixs2[row][col]) for col in range(alt)] for
            row in range(alt)]
        jump = [[sg.Text("")]]
        Summat = [[sg.Text("Summation:")]]
        bottom = [[sg.Text(alternatives[row])] + [sg.Text("=")] + [sg.Text(rs2[row]) for col in range(1)] for row
                  in range(alt)]
        jump2 = [[sg.Text("")]]
        order = [[sg.Text(alternatives0[col]) for col in range(len(alternatives0))] + [sg.Text("- Original")] for
                 row in range(1)]
        layout = header + input_rows + jump + Summat + bottom + jump2 + order
        layout += [[sg.Button("Send")]]
        window = sg.Window('Results of S2', layout, font='Courier 12')
        event, values = window.Read()
        window.close()
    alternatives0 = []
    tca2 = 0
    ver2 = 0
    meter += 1
meter = 0;
weight3 = []
for i in range(cri):
    weight[i] = weight4[i]
    weight2[i] = weight4[i]
# S3
while meter < 1:
    c = [];
    b = [];
    e = [];
    f = [];
    g = [];
    h = [];
    x = 0;
    y = 0;
    w = 0;
    z = 0;
    v = 0;
    t = 0;
    rs3 = [];
    rs3o = []
    if meter != 0:
        lower = max(weight2)
        for j in range(cri):
            if weight2[j] < lower and weight2.index(lower) not in weight3 and weight2[j] > 0:
                lower = weight2[j]
        weight3.append(weight2.index(lower))
        weight2[weight2.index(lower)] = 0
        weight[weight3[meter - 1]] = 0
    for i in range(alt):
        for j in range(alt):
            if (i < j):
                for k in range(cri):
                    x = compare(matrix[i][k], matrix[j][k])
                    y = dif(matrix[i][k], matrix[j][k])
                    w = compare(matrix[j][k], matrix[i][k])
                    z = dif(matrix[j][k], matrix[i][k])
                    v = ind(pertinence[k], pertinence2[i][k], pertinence2[j][k])
                    t = ind(pertinence[k], pertinence2[j][k], pertinence2[i][k])
                    b.append(y)
                    c.append(x)
                    e.append(w)
                    f.append(z)
                    g.append(v)
                    h.append(t)
                if (s3(c, b, g) == "dominates") and (s3(e, f, h) == "dominates"):
                    if (discordances3(b, c, g) == 0.5) or (discordances3(f, e, h) == 0.5):
                        matrixs3[i][j] = 0.5
                        matrixs3[j][i] = 0.5
                    else:
                        matrixs3[i][j] = round(discordances3(b, c, g), 3)
                        matrixs3[j][i] = round(discordances3(f, e, h), 3)
                elif (s3(c, b, g) == "dominates") and (s3(e, f, h) != "dominates"):
                    if (discordances3(b, c, g) != 0.5):
                        matrixs3[i][j] = round(ms3, 3)
                        matrixs3[j][i] = 0
                    else:
                        matrixs3[i][j] = 0.5
                        matrixs3[j][i] = 0.5
                elif (s3(c, b, g) != "dominates") and (s3(e, f, h) == "dominates"):
                    if (discordances3(f, e, h) != 0.5):
                        matrixs3[i][j] = 0
                        matrixs3[j][i] = round(ms3, 3)
                    else:
                        matrixs3[i][j] = 0.5
                        matrixs3[j][i] = matrixs3[i][j]
                else:
                    matrixs3[i][j] = 0.5
                    matrixs3[j][i] = matrixs3[i][j]
                c = [];
                b = [];
                e = [];
                f = [];
                g = [];
                h = []
    for i in range(alt):
        r3 = 0.0
        for j in range(alt):
            r3 += matrixs3[i][j]
        rs3.append(round(r3, 3))
    for i in range(len(rs3)):
        rs3o.append(rs3[i])
    rs3o.sort()
    rs3o.reverse()
    for i in range(alt):
        for j in range(alt):
            if rs3o[i] == rs3[j]:
                if alternatives[j] in alternatives0:
                    "nothing"
                else:
                    alternatives0.append(alternatives[j])
    for i in range(alt):
        if (i != alt - 1):
            if rs3o[i] > rs3o[i + 1]:
                alternatives0.insert(2 * i + 1, ">")
                if meter == 0:
                    originals3.append(alternatives0[2 * i])
                    originals3.append(">")
            elif rs3o[i] == rs3o[i + 1]:
                alternatives0.insert(2 * i + 1, "=")
                if meter == 0:
                    originals3.append(alternatives0[2 * i])
                    originals3.append("=")
        else:
            if meter == 0:
                originals3.append(alternatives0[2 * i])
    if meter == 0:
        header = [[sg.Text('S3', justification='center', size=(35, 1), font=('Any', 20, 'bold'))]]
        input_rows = [
            [sg.Text(alternatives[row])] + [sg.Text("-")] + [sg.Text(matrixs3[row][col]) for col in range(alt)] for
            row in range(alt)]
        jump = [[sg.Text("")]]
        Summat = [[sg.Text("Summation:")]]
        bottom = [[sg.Text(alternatives[row])] + [sg.Text("=")] + [sg.Text(rs3[row]) for col in range(1)] for row
                  in range(alt)]
        jump2 = [[sg.Text("")]]
        order = [[sg.Text(alternatives0[col]) for col in range(len(alternatives0))] + [sg.Text("- Original")] for
                 row in range(1)]
        layout = header + input_rows + jump + Summat + bottom + jump2 + order
        layout += [[sg.Button("Send")]]
        window = sg.Window('Results of S3', layout, font='Courier 12')
        event, values = window.Read()
        window.close()
    alternatives0 = []
    tca3 = 0
    ver3 = 0
    meter += 1
head = [[sg.Text("Do you want to use RST?", size=(26, 0))]]
radio = [[sg.Radio("Yes", "continue", key="yes2")] + [sg.Radio("No", "continue", key="no2")]]
layout = head + radio
layout += [[sg.Button("Send data")]]
window = sg.Window('RST', layout, font='Courier 12')
event, values = window.Read()
window.close()
yes2 = values["yes2"]
no2 = values["no2"]
cris1 = []
cris2 = []
cris3 = []
if yes2 == True:
    usetca = 0
elif no2 == True:
    usetca = 1
# S1 TCA
if usetca != 1:
    meter = 1;
    weight3 = []
    c = [];
    b = [];
    e = [];
    f = [];
    g = [];
    h = [];
    lower = max(weight)
    while meter < cri + 1:
        c = [];
        b = [];
        e = [];
        f = [];
        g = [];
        h = [];
        x = 0;
        y = 0;
        w = 0;
        z = 0;
        v = 0;
        t = 0;
        rs1 = [];
        rs1o = [];
        if meter != 0 and usetca != 1:
            lower = max(weight2)
            for j in range(cri):
                if weight2[j] < lower and weight2.index(lower) not in weight3 and weight2[j] > 0:
                    lower = weight2[j]
            weight3.append(weight2.index(lower))
            weight2[weight2.index(lower)] = 0
            weight[weight3[meter - 1]] = 0
        for i in range(alt):
            for j in range(alt):
                if (i < j):
                    for k in range(cri):
                        x = compare(matrix[i][k], matrix[j][k])
                        y = dif(matrix[i][k], matrix[j][k])
                        w = compare(matrix[j][k], matrix[i][k])
                        z = dif(matrix[j][k], matrix[i][k])
                        v = ind(pertinence[k], pertinence2[i][k], pertinence2[j][k])
                        t = ind(pertinence[k], pertinence2[j][k], pertinence2[i][k])
                        b.append(y)
                        c.append(x)
                        e.append(w)
                        f.append(z)
                        g.append(v)
                        h.append(t)
                    if (s1(c, b, g) == "dominates") and (s1(e, f, h) == "dominates"):
                        if (discordances1(b, c, g) == 0.5) or (discordances1(f, e, h) == 0.5):
                            matrixs1[i][j] = 0.5
                            matrixs1[j][i] = 0.5
                        else:
                            matrixs1[i][j] = round(discordances1(b, c, g), 3)
                            matrixs1[j][i] = round(discordances1(f, e, h), 3)
                    elif (s1(c, b, g) == "dominates") and (s1(e, f, h) != "dominates"):
                        if (discordances1(b, c, g) != 0.5):
                            matrixs1[i][j] = round(ms1, 3)
                            matrixs1[j][i] = 0
                        else:
                            matrixs1[i][j] = 0.5
                            matrixs1[j][i] = 0.5
                    elif (s1(c, b, g) != "dominates") and (s1(e, f, h) == "dominates"):
                        if (discordances1(f, e, h) != 0.5):
                            matrixs1[i][j] = 0
                            matrixs1[j][i] = round(ms1, 3)
                        else:
                            matrixs1[i][j] = 0.5
                            matrixs1[j][i] = matrixs1[i][j]
                    else:
                        matrixs1[i][j] = 0.5
                        matrixs1[j][i] = matrixs1[i][j]
                    c = [];
                    b = [];
                    e = [];
                    f = []
        for i in range(alt):
            r1 = 0.0
            for j in range(alt):
                r1 += matrixs1[i][j]
            rs1.append(round(r1, 3))
        for i in range(len(rs1)):
            rs1o.append(rs1[i])
        rs1o.sort()
        rs1o.reverse()
        for i in range(alt):
            for j in range(alt):
                if rs1o[i] == rs1[j]:
                    if alternatives[j] in alternatives0:
                        "nothing"
                    else:
                        alternatives0.append(alternatives[j])
        for i in range(alt):
            if (i != alt - 1):
                if rs1o[i] > rs1o[i + 1]:
                    alternatives0.insert(2 * i + 1, ">")
                    if meter == 0:
                        originals1.append(alternatives0[2 * i])
                        originals1.append(">")
                elif rs1o[i] == rs1o[i + 1]:
                    alternatives0.insert(2 * i + 1, "=")
                    if meter == 0:
                        originals1.append(alternatives0[2 * i])
                        originals1.append("=")
            else:
                if meter == 0:
                    originals1.append(alternatives0[2 * i])
        if meter == 0:
            header = [[sg.Text('S1', justification='center', size=(35, 1), font=('Any', 20, 'bold'))]]
            input_rows = [
                [sg.Text(alternatives[row])] + [sg.Text("-")] + [sg.Text(matrixs1[row][col]) for col in range(alt)]
                for row in range(alt)]
            jump = [[sg.Text("")]]
            Summat = [[sg.Text("Summation:")]]
            bottom = [[sg.Text(alternatives[row])] + [sg.Text("=")] + [sg.Text(rs1[row]) for col in range(1)] for
                      row in range(alt)]
            jump2 = [[sg.Text("")]]
            order = [[sg.Text(alternatives0[col]) for col in range(len(alternatives0))] + [sg.Text("- Original")]
                     for row in range(1)]
            layout = header + input_rows + jump + Summat + bottom + jump2 + order
            layout += [[sg.Button("Send")]]
            window = sg.Window('Results of S1', layout, font='Courier 12')
            event, values = window.Read()
            window.close()
        elif meter != 0 and usetca != 1:
            sg.Popup("Analyzing the criteria " + criteria[weight3[meter - 1]])
            header = [[sg.Text('S1', justification='center', size=(35, 1), font=('Any', 20, 'bold'))]]
            input_rows = [
                [sg.Text(alternatives[row])] + [sg.Text("-")] + [sg.Text(matrixs1[row][col]) for col in range(alt)]
                for row in range(alt)]
            jump = [[sg.Text("")]]
            Summat = [[sg.Text("Summation:")]]
            bottom = [[sg.Text(alternatives[row])] + [sg.Text("=")] + [sg.Text(rs1[row]) for col in range(1)] for
                      row in range(alt)]
            jump2 = [[sg.Text("")]]
            order = [
                [sg.Text(alternatives0[col]) for col in range(len(alternatives0))] + [sg.Text("- Without the criteria")]
                for row in range(1)]
            order2 = [[sg.Text(originals1[col]) for col in range(len(originals1))] + [sg.Text("- Original")] for
                      row in range(1)]
            layout = header + input_rows + jump + Summat + bottom + jump2 + order + order2
            layout += [[sg.Button("Send")]]
            window = sg.Window('Results of S1', layout, font='Courier 12')
            event, values = window.Read()
            window.close()
        if meter != 0 and usetca != 1:
            for i in range(len(alternatives0)):
                if alternatives0[i] == originals1[i]:
                    tca1 += 1
            if (tca1 == len(alternatives0)):
                sg.Popup("Criterion " + criteria[weight3[meter - 1]] + " can be removed.")
                cris1.append(criteria[weight3[meter - 1]])
                if (criteria[weight3[meter - 1]]) not in cristotal:
                    cristotal.append(criteria[weight3[meter - 1]])
                ver1 = 1
        if meter != 0 and usetca != 1:
            if ver1 != 1:
                weight[weight3[meter - 1]] = weight4[weight3[meter - 1]]
        alternatives0 = []
        tca1 = 0
        ver1 = 0
        meter += 1
    if usetca != 1:
        if len(cris1) == 0:
            sg.Popup("RST result for S1:", "No criteria can be removed.")
        elif len(cris1) == 1:
            sg.Popup("RST result for S1:", "The criteria that can be removed are:", cris1[0])
        else:
            header = [[sg.Text("RST result for S1:")]]
            head = [[sg.Text("The criteria that can be removed are:")]]
            order = [[sg.Text(cris1[row]) for col in range(1)] for row in range(len(cris1))]
            layout = head + header + order
            layout += [[sg.Button("Send")]]
            window = sg.Window('Results of S1', layout, font='Courier 12')
            event, values = window.Read()
            window.close()
    meter = 1;
    weight3 = []
    for i in range(cri):
        weight[i] = weight4[i]
        weight2[i] = weight4[i]
# S2 TCA
if usetca != 1:
    while meter < cri + 1:
        c = [];
        b = [];
        e = [];
        f = [];
        g = [];
        h = [];
        x = 0;
        y = 0;
        w = 0;
        z = 0;
        v = 0;
        t = 0;
        rs2 = [];
        rs2o = []
        if meter != 0 and usetca != 1:
            lower = max(weight2)
            for j in range(cri):
                if weight2[j] < lower and weight2.index(lower) not in weight3 and weight2[j] > 0:
                    lower = weight2[j]
            weight3.append(weight2.index(lower))
            weight2[weight2.index(lower)] = 0
            weight[weight3[meter - 1]] = 0
        for i in range(alt):
            for j in range(alt):
                if (i < j):
                    for k in range(cri):
                        x = compare(matrix[i][k], matrix[j][k])
                        y = dif(matrix[i][k], matrix[j][k])
                        w = compare(matrix[j][k], matrix[i][k])
                        z = dif(matrix[j][k], matrix[i][k])
                        v = ind(pertinence[k], pertinence2[i][k], pertinence2[j][k])
                        t = ind(pertinence[k], pertinence2[j][k], pertinence2[i][k])
                        b.append(y)
                        c.append(x)
                        e.append(w)
                        f.append(z)
                        g.append(v)
                        h.append(t)
                    if (s2(c, b, g) == "dominates") and (s2(e, f, h) == "dominates"):
                        if (discordances2(b, c, g) == 0.5) or (discordances2(f, e, h) == 0.5):
                            matrixs2[i][j] = 0.5
                            matrixs2[j][i] = 0.5
                        else:
                            matrixs2[i][j] = round(discordances2(b, c, g), 3)
                            matrixs2[j][i] = round(discordances2(f, e, h), 3)
                    elif (s2(c, b, g) == "dominates") and (s2(e, f, h) != "dominates"):
                        if (discordances2(b, c, g) != 0.5):
                            matrixs2[i][j] = round(ms2, 3)
                            matrixs2[j][i] = 0
                        else:
                            matrixs2[i][j] = 0.5
                            matrixs2[j][i] = 0.5
                    elif (s2(c, b, g) != "dominates") and (s2(e, f, h) == "dominates"):
                        if (discordances2(f, e, h) != 0.5):
                            matrixs2[i][j] = 0
                            matrixs2[j][i] = round(ms2, 3)
                        else:
                            matrixs2[i][j] = 0.5
                            matrixs2[j][i] = matrixs2[i][j]
                    else:
                        matrixs2[i][j] = 0.5
                        matrixs2[j][i] = matrixs2[i][j]
                    c = [];
                    b = [];
                    e = [];
                    f = []
        for i in range(alt):
            r2 = 0.0
            for j in range(alt):
                r2 += matrixs2[i][j]
            rs2.append(round(r2, 3))
        for i in range(len(rs2)):
            rs2o.append(rs2[i])
        rs2o.sort()
        rs2o.reverse()
        for i in range(alt):
            for j in range(alt):
                if rs2o[i] == rs2[j]:
                    if alternatives[j] in alternatives0:
                        "nothing"
                    else:
                        alternatives0.append(alternatives[j])
        for i in range(alt):
            if (i != alt - 1):
                if rs2o[i] > rs2o[i + 1]:
                    alternatives0.insert(2 * i + 1, ">")
                    if meter == 0:
                        originals2.append(alternatives0[2 * i])
                        originals2.append(">")
                elif rs2o[i] == rs2o[i + 1]:
                    alternatives0.insert(2 * i + 1, "=")
                    if meter == 0:
                        originals2.append(alternatives0[2 * i])
                        originals2.append("=")
            else:
                if meter == 0:
                    originals2.append(alternatives0[2 * i])
        if meter == 0:
            header = [[sg.Text('S2', justification='center', size=(35, 1), font=('Any', 20, 'bold'))]]
            input_rows = [
                [sg.Text(alternatives[row])] + [sg.Text("-")] + [sg.Text(matrixs2[row][col]) for col in range(alt)]
                for row in range(alt)]
            jump = [[sg.Text("")]]
            Summat = [[sg.Text("Summation:")]]
            bottom = [[sg.Text(alternatives[row])] + [sg.Text("= ")] + [sg.Text(rs2[row]) for col in range(1)] for
                      row in range(alt)]
            jump2 = [[sg.Text("")]]
            order = [[sg.Text(alternatives0[col]) for col in range(len(alternatives0))] + [sg.Text("- Original")]
                     for row in range(1)]
            layout = header + input_rows + jump + Summat + bottom + jump2 + order
            layout += [[sg.Button("Send")]]
            window = sg.Window('Results of S2', layout, font='Courier 12')
            event, values = window.Read()
            window.close()
        elif meter != 0 and usetca != 1:
            sg.Popup("Analyzing the criteria " + criteria[weight3[meter - 1]])
            header = [[sg.Text('S2', justification='center', size=(35, 1), font=('Any', 20, 'bold'))]]
            input_rows = [
                [sg.Text(alternatives[row])] + [sg.Text("-")] + [sg.Text(matrixs2[row][col]) for col in range(alt)]
                for row in range(alt)]
            jump = [[sg.Text("")]]
            Summat = [[sg.Text("Summation:")]]
            bottom = [[sg.Text(alternatives[row])] + [sg.Text("=")] + [sg.Text(rs2[row]) for col in range(1)] for
                      row in range(alt)]
            jump2 = [[sg.Text("")]]
            order = [
                [sg.Text(alternatives0[col]) for col in range(len(alternatives0))] + [sg.Text("- Without the criteria")]
                for row in range(1)]
            order2 = [[sg.Text(originals2[col]) for col in range(len(originals2))] + [sg.Text("- Original")] for
                      row in range(1)]
            layout = header + input_rows + jump + Summat + bottom + jump2 + order + order2
            layout += [[sg.Button("Send")]]
            window = sg.Window('Results of S2', layout, font='Courier 12')
            event, values = window.Read()
            window.close()
        if meter != 0 and usetca != 1:
            for i in range(len(alternatives0)):
                if alternatives0[i] == originals2[i]:
                    tca2 += 1
            if (tca2 == len(alternatives0)):
                sg.Popup("Criterion " + criteria[weight3[meter - 1]] + " can be removed.")
                cris2.append(criteria[weight3[meter - 1]])
                if (criteria[weight3[meter - 1]]) not in cristotal:
                    cristotal.append(criteria[weight3[meter - 1]])
                ver2 = 1
        if meter != 0 and usetca != 1:
            if ver2 != 1:
                weight[weight3[meter - 1]] = weight4[weight3[meter - 1]]
        alternatives0 = []
        tca2 = 0
        ver2 = 0
        meter += 1
    if usetca != 1:
        if len(cris2) == 0:
            sg.Popup("RST result for S2:", "No criteria can be removed.")
        elif len(cris2) == 1:
            sg.Popup("RST result for S2:", "The criteria that can be removed are:", cris2[0])
        else:
            header = [[sg.Text("RST result for S2:")]]
            head = [[sg.Text("The criteria that can be removed are:")]]
            order = [[sg.Text(cris2[row]) for col in range(1)] for row in range(len(cris2))]
            layout = head + header + order
            layout += [[sg.Button("Send")]]
            window = sg.Window('Results of S2', layout, font='Courier 12')
            event, values = window.Read()
            window.close()
    meter = 1;
    weight3 = []
    for i in range(cri):
        weight[i] = weight4[i]
        weight2[i] = weight4[i]
# S3 TCA
if usetca != 1:
    while meter < cri + 1:
        c = [];
        b = [];
        e = [];
        f = [];
        g = [];
        h = [];
        x = 0;
        y = 0;
        w = 0;
        z = 0;
        v = 0;
        t = 0;
        rs3 = [];
        rs3o = []
        if meter != 0 and usetca != 1:
            lower = max(weight2)
            for j in range(cri):
                if weight2[j] < lower and weight2.index(lower) not in weight3 and weight2[j] > 0:
                    lower = weight2[j]
            weight3.append(weight2.index(lower))
            weight2[weight2.index(lower)] = 0
            weight[weight3[meter - 1]] = 0
        for i in range(alt):
            for j in range(alt):
                if (i < j):
                    for k in range(cri):
                        x = compare(matrix[i][k], matrix[j][k])
                        y = dif(matrix[i][k], matrix[j][k])
                        w = compare(matrix[j][k], matrix[i][k])
                        z = dif(matrix[j][k], matrix[i][k])
                        v = ind(pertinence[k], pertinence2[i][k], pertinence2[j][k])
                        t = ind(pertinence[k], pertinence2[j][k], pertinence2[i][k])
                        b.append(y)
                        c.append(x)
                        e.append(w)
                        f.append(z)
                        g.append(v)
                        h.append(t)
                    if (s3(c, b, g) == "dominates") and (s3(e, f, h) == "dominates"):
                        if (discordances3(b, c, g) == 0.5) or (discordances3(f, e, h) == 0.5):
                            matrixs3[i][j] = 0.5
                            matrixs3[j][i] = 0.5
                        else:
                            matrixs3[i][j] = round(discordances3(b, c, g), 3)
                            matrixs3[j][i] = round(discordances3(f, e, h), 3)
                    elif (s3(c, b, g) == "dominates") and (s3(e, f, h) != "dominates"):
                        if (discordances3(b, c, g) != 0.5):
                            matrixs3[i][j] = round(ms3, 3)
                            matrixs3[j][i] = 0
                        else:
                            matrixs3[i][j] = 0.5
                            matrixs3[j][i] = 0.5
                    elif (s3(c, b, g) != "dominates") and (s3(e, f, h) == "dominates"):
                        if (discordances3(f, e, h) != 0.5):
                            matrixs3[i][j] = 0
                            matrixs3[j][i] = round(ms3, 3)
                        else:
                            matrixs3[i][j] = 0.5
                            matrixs3[j][i] = matrixs3[i][j]
                    else:
                        matrixs3[i][j] = 0.5
                        matrixs3[j][i] = matrixs3[i][j]
                    c = [];
                    b = [];
                    e = [];
                    f = []
        for i in range(alt):
            r3 = 0.0
            for j in range(alt):
                r3 += matrixs3[i][j]
            rs3.append(round(r3, 3))
        for i in range(len(rs3)):
            rs3o.append(rs3[i])
        rs3o.sort()
        rs3o.reverse()
        for i in range(alt):
            for j in range(alt):
                if rs3o[i] == rs3[j]:
                    if alternatives[j] in alternatives0:
                        "nothing"
                    else:
                        alternatives0.append(alternatives[j])
        for i in range(alt):
            if (i != alt - 1):
                if rs3o[i] > rs3o[i + 1]:
                    alternatives0.insert(2 * i + 1, ">")
                    if meter == 0:
                        originals3.append(alternatives0[2 * i])
                        originals3.append(">")
                elif rs3o[i] == rs3o[i + 1]:
                    alternatives0.insert(2 * i + 1, "=")
                    if meter == 0:
                        originals3.append(alternatives0[2 * i])
                        originals3.append("=")
            else:
                if meter == 0:
                    originals3.append(alternatives0[2 * i])
        if meter == 0:
            header = [[sg.Text('S3', justification='center', size=(35, 1), font=('Any', 20, 'bold'))]]
            input_rows = [
                [sg.Text(alternatives[row])] + [sg.Text("-")] + [sg.Text(matrixs3[row][col]) for col in range(alt)]
                for row in range(alt)]
            jump = [[sg.Text("")]]
            Summat = [[sg.Text("Summation:")]]
            bottom = [[sg.Text(alternatives[row])] + [sg.Text("=")] + [sg.Text(rs3[row]) for col in range(1)] for
                      row in range(alt)]
            jump2 = [[sg.Text("")]]
            order = [[sg.Text(alternatives0[col]) for col in range(len(alternatives0))] + [sg.Text("- Original")]
                     for row in range(1)]
            layout = header + input_rows + jump + Summat + bottom + jump2 + order
            layout += [[sg.Button("Send")]]
            window = sg.Window('Results of S3', layout, font='Courier 12')
            event, values = window.Read()
            window.close()
        elif meter != 0 and usetca != 1:
            sg.Popup("Analyzing the criteria " + criteria[weight3[meter - 1]])
            header = [[sg.Text('S3', justification='center', size=(35, 1), font=('Any', 20, 'bold'))]]
            input_rows = [
                [sg.Text(alternatives[row])] + [sg.Text("-")] + [sg.Text(matrixs3[row][col]) for col in range(alt)]
                for row in range(alt)]
            jump = [[sg.Text("")]]
            Summat = [[sg.Text("Summation:")]]
            bottom = [[sg.Text(alternatives[row])] + [sg.Text("=")] + [sg.Text(rs3[row]) for col in range(1)] for
                      row in range(alt)]
            jump2 = [[sg.Text("")]]
            order = [
                [sg.Text(alternatives0[col]) for col in range(len(alternatives0))] + [sg.Text("- Without the criteria")]
                for row in range(1)]
            order2 = [[sg.Text(originals3[col]) for col in range(len(originals3))] + [sg.Text("- Original")] for
                      row in range(1)]
            layout = header + input_rows + jump + Summat + bottom + jump2 + order + order2
            layout += [[sg.Button("Send")]]
            window = sg.Window('Results of S3', layout, font='Courier 12')
            event, values = window.Read()
            window.close()
        if meter != 0 and usetca != 1:
            for i in range(len(alternatives0)):
                if alternatives0[i] == originals3[i]:
                    tca3 += 1
            if (tca3 == len(alternatives0)):
                sg.Popup("Criterion " + criteria[weight3[meter - 1]] + " can be removed.")
                cris3.append(criteria[weight3[meter - 1]])
                if (criteria[weight3[meter - 1]]) not in cristotal:
                    cristotal.append(criteria[weight3[meter - 1]])
                ver3 = 1
        if meter != 0 and usetca != 1:
            if ver3 != 1:
                weight[weight3[meter - 1]] = weight4[weight3[meter - 1]]
        alternatives0 = []
        tca3 = 0
        ver3 = 0
        meter += 1
    if usetca != 1:
        if len(cris3) == 0:
            sg.Popup("RST result for S3:", "No criteria can be removed.")
        elif len(cris3) == 1:
            sg.Popup("RST result for S3:", "The criteria that can be removed are:", cris3[0])
        else:
            header = [[sg.Text("RST result for S3:")]]
            head = [[sg.Text("The criteria that can be removed are:")]]
            order = [[sg.Text(cris3[row]) for col in range(1)] for row in range(len(cris3))]
            layout = head + header + order
            layout += [[sg.Button("Send")]]
            window = sg.Window('Results of S3', layout, font='Courier 12')
            event, values = window.Read()
            window.close()
originals1 = []
originals2 = []
originals3 = []
# TCA Nebula
if usepert == 0:
    if usetca != 1:
        head = [[sg.Text("Do you want to use FRST?", size=(26, 0))]]
        radio = [[sg.Radio("Yes", "continue", key="yes2")] + [sg.Radio("No", "continue", key="no2")]]
        layout = head + radio
        layout += [[sg.Button("Send data")]]
        window = sg.Window('FRST', layout, font='Courier 12')
        event, values = window.Read()
        window.close()
        yes2 = values["yes2"]
        no2 = values["no2"]
        if yes2 == True:
            usarneb = 0
        elif no2 == True:
            usarneb = 1
        if usarneb == 0:
            col_width = 9
            val_width = 6
            header = [[sg.Text('Original FRST', justification='center', expand_x=True, font=('Any', 20, 'bold'))]]
            jump = [[sg.Text("")]]
            head = [
                [sg.Text(" ")] +
                [sg.Text("Weights", size=(col_width, 1), justification='center')] +
                [sg.Text("-", size=(3, 1), justification='center')] +
                [sg.Text(f"{pertinence[col]:.1f}", size=(val_width, 1), justification='center') for col in
                 range(cri)]
            ]
            input_rows = [
                [sg.Text(" ")] +
                [sg.Text(alternatives[row], size=(col_width, 1), justification='center')] +
                [sg.Text("-", size=(3, 1), justification='center')] +
                [sg.Text(f"{pertinence2[row][col]:.2f}", size=(val_width, 1), justification='center') for col in
                 range(cri)]
                for row in range(alt)
            ]
            jump2 = [[sg.Text("")]]
            averages = [
                [sg.Text("Average weights:", justification='left')] +
                [sg.Text(f"{medtcan[0]:.2f}", justification='center')]
            ]
            averagealt = [
                [sg.Text("Average of", justification='left')] +
                [sg.Text(alternatives[row], justification='center')] +
                [sg.Text("-", justification='center')] +
                [sg.Text(f"{medtcan[row + 1]:.3f}", justification='center')]
                for row in range(alt)
            ]
            avaverage = [
                [sg.Text("Average weights with", justification='left')] +
                [sg.Text(alternatives[row], justification='center')] +
                [sg.Text("-", justification='center')] +
                [sg.Text(f"{medtcan[row + 1 + alt]:.3f}", justification='center')]
                for row in range(alt)
            ]
            layout = header + jump + head + input_rows + jump2 + averages + averagealt + avaverage + [
                [sg.Button("OK")]]
            window = sg.Window('FRST - Original', layout, font='Courier 12', resizable=True, finalize=True)
            event, values = window.read()
            window.close()

            for f in range(len(cristotal)):
                neb = 0
                rtcan = []
                rt2 = []
                pos = criteria.index(cristotal[f])
                pertinence.pop(pos)
                z = round(average(pertinence), 4)
                rtcan.append(z)
                for k in range(alt):
                    pertinence2[k].pop(pos)
                    z = round(average(pertinence2[k]), 4)
                    rtcan.append(z)
                    z = round(((rtcan[k + 1] + rtcan[0]) / 2), 4)
                    rt2.append(z)

                col_width = 9
                val_width = 6
                header = [
                    [sg.Text(f'Removing criterion {cristotal[f]}', justification='center', expand_x=True, font=('Any', 20, 'bold'))]
                ]
                jump = [[sg.Text("")]]
                head = [
                    [sg.Text(" ")] +
                    [sg.Text("Weights", size=(col_width, 1), justification='center')] +
                    [sg.Text("-", size=(3, 1), justification='center')] +
                    [sg.Text(f"{pertinence[col]:.2f}", size=(val_width, 1), justification='center') for col in
                     range(len(pertinence))]
                ]
                input_rows = [
                    [sg.Text(" ")] +
                    [sg.Text(alternatives[row], size=(col_width, 1), justification='center')] +
                    [sg.Text("-", size=(3, 1), justification='center')] +
                    [sg.Text(f"{pertinence2[row][col]:.2f}", size=(val_width, 1), justification='center') for
                     col in
                     range(len(pertinence))]
                    for row in range(alt)
                ]
                jump2 = [[sg.Text("")]]
                averages = [
                    [sg.Text("Average weights:", justification='left')] +
                    [sg.Text(f"{rtcan[0]:.1f}", justification='center')]
                ]
                averagealt = [
                    [sg.Text("Average of", justification='left')] +
                    [sg.Text(alternatives[row], justification='center')] +
                    [sg.Text("-", justification='center')] +
                    [sg.Text(f"{rtcan[row + 1]:.3f}", justification='center') for col in range(1)]
                    for row in range(alt)
                ]
                avaverage = [
                    [sg.Text("Average weights with", justification='left')] +
                    [sg.Text(alternatives[row], justification='center')] +
                    [sg.Text("-", justification='center')] +
                    [sg.Text(f"{rt2[row]:.3f}", justification='center') for col in range(1)]
                    for row in range(alt)
                ]
                layout = header + jump + head + input_rows + jump2 + averages + averagealt + avaverage
                layout += [[sg.Button("OK")]]
                window = sg.Window('FRST - Original', layout, font='Courier 12')
                event, values = window.Read()
                window.close()

                for k in range(alt):
                    pertinence2[k].insert(pos, pertinence2tca[k][pos])
                pertinence.insert(pos, pertinencetca[pos])
                for j in range(len(rt2)):
                    rtcan.append(rt2[j])
                for j in range(len(rtcan)):
                    if rtcan[j] >= medtcan[j] and rtcan != medtcan:
                        neb += 1
                if neb == len(rtcan):
                    tcaneb.append(cristotal[f])
            if len(tcaneb) == 1:
                sg.Popup("Using the FRST, the criteria can be removed:", tcaneb[0])
            elif len(tcaneb) == 0:
                sg.Popup("Using the FRST, no criteria can be removed.")
            elif len(tcaneb) > 1:
                header = [[sg.Text('Using the FRST, the following criteria can be removed:')]]
                head = [[sg.Text(tcaneb[row]) for col in range(1)] for row in range(len(tcaneb))]
                layout = header + head
                layout += [[sg.Button("OK")]]
                window = sg.Window('FRST', layout, font='Courier 12')
                event, values = window.Read()
                window.close()
            tcaneb = []
layout_popup = [[sg.Text("The program has been terminated, thank you for using BWM THOR2")]]
window_popup = sg.Window('Good Bye', layout_popup)
window_popup.read(timeout=1500)
window_popup.close()
plt.close("all")
gc.collect()