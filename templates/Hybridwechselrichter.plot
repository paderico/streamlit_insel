# PART I : Variables that could be set by PLOT Block. If not set by PLOT Block, should be set to ""
title   = "Strombezug des Gebäudes"
x_label  = ""
x_unit   = ""
x_format = "" # Can be empty, but needs to be a string

x_min    = "" # Can be empty, but needs to be a string
x_max    = "" # Can be empty, but needs to be a string
x_tics   = "" # Can be empty, but needs to be a string
mx_tics  = "" # Can be empty, but needs to be a string

y_label  = "Uhrzeit des Tages"
y_unit   = ""
y_format = "%g:00" # Can be empty, but needs to be a string

y_min    = "0" # Can be empty, but needs to be a string
y_max    = "23" # Can be empty, but needs to be a string
y_tics   = "3" # Can be empty, but needs to be a string
my_tics  = "2" # Can be empty, but needs to be a string

chosen_terminal = 1 # 0 for window output, 1 for png, 2 for pdf, 3 for svg, 4 for txt, 5 for tex, 6 for eps
window_output = (chosen_terminal == 0)
png_output = (chosen_terminal == 1)
pdf_output = (chosen_terminal == 2)
svg_output = (chosen_terminal == 3)
txt_output = (chosen_terminal == 4)
tex_output = (chosen_terminal == 5)
eps_output = (chosen_terminal == 6)

output_filename = '/tmp/Hybridwechselrichter.png' # Needs to be defined if chosen_terminal > 0

width = 1152 # Needs to be defined
height = 768 # Needs to be defined

show_grid = 0

axis_thickness = "1"

font_name = "Calibri"
font_size = 18
font_style = ""
cb_label  = "Netzbezug"
cb_unit   = "Wh / 5min"
cb_format = "" # Can be empty, but needs to be a string

cb_min    = "0" # Can be empty, but needs to be a string
cb_max    = "350" # Can be empty, but needs to be a string
cb_tics   = "" # Can be empty, but needs to be a string
mcb_tics  = "" # Can be empty, but needs to be a string

show_colorbox = 1
show_contour = 0

# PART III : Customize the plot depending on variables defined in PART I
data_file = "~/.insel_8_3/tmp/insel.gpl"
model_dir = "app/templates"
set title title

set sample 1000
if (show_grid) set grid linewidth axis_thickness

# Check if pngcairo is installed, use png otherwise
if (strstrt(GPVAL_TERMINALS, 'pngcairo') > 0)\
  png_or_pngcairo = "pngcairo";\
else \
  png_or_pngcairo = "png"

# Check if pdfcairo is installed, use pdf otherwise
if (strstrt(GPVAL_TERMINALS, 'pdfcairo') > 0)\
  pdf_or_pdfcairo = "pdfcairo";\
else \
  pdf_or_pdfcairo = "pdf"

font_description = sprintf('%s%s, %d',font_name, font_style, font_size)

if (png_output)\
  set terminal png_or_pngcairo font font_description linewidth axis_thickness size width, height
if (pdf_output)\
  set terminal pdf_or_pdfcairo font font_description linewidth axis_thickness*1.5 size width/180.0, height/180.0
if (txt_output)\
  set terminal dumb size width/8, height/20
if (tex_output)\
  set terminal epslatex standalone color linewidth axis_thickness size width/180.0, height/180.0 header "\\usepackage[utf8x]{inputenc}"
if (svg_output)\
  set terminal svg size width, height font font_description linewidth axis_thickness;\
  set encoding utf8
if (eps_output)\
  set terminal epscairo font font_description size width, height
if (!window_output)\
  set output output_filename
if (window_output)\
  set border linewidth axis_thickness;\
  set terminal wxt font font_description size width, height position 30, 30

if (x_unit ne "")\
  set xlabel sprintf("%s [%s]", x_label, x_unit);\
else\
  set xlabel x_label

if (x_min ne "") set xrange [x_min:]
if (x_max ne "") set xrange [:x_max]
if (x_tics ne ""){
  set xtics x_tics
} else {
  set xtics autofreq
}
if (mx_tics ne "") set mxtics mx_tics
if (x_format ne "") set format x x_format

if (y_unit ne "")\
  set ylabel sprintf("%s [%s]", y_label, y_unit);\
else\
  set ylabel y_label

if (y_min ne "") set yrange [y_min:]
if (y_max ne "") set yrange [:y_max]
if (y_tics ne ""){
  set ytics y_tics
} else {
  set ytics autofreq
}
if (my_tics ne "") set mytics my_tics
if (y_format ne "") set format y y_format

if (cb_unit ne "")\
  set cblabel sprintf("%s [%s]", cb_label, cb_unit);\
else\
  set cblabel cb_label

if (cb_min ne "") set cbrange [cb_min:]
if (cb_max ne "") set cbrange [:cb_max]
if (cb_tics ne ""){
  set cbtics cb_tics
} else {
  set cbtics autofreq
}
if (mcb_tics ne "") set mcbtics mcb_tics
if (cb_format ne "") set format cb cb_format

set pm3d
set palette defined ( 0 '#3288BD', 1 '#66C2A5', 2 '#ABDDA4', 3 '#E6F598', 4 '#FEE08B', 5 '#FDAE61', 6 '#F46D43', 7 '#D53E4F')
unset surface
if (show_grid) set grid xtics ytics mxtics mytics
if (show_colorbox)\
  set colorbox;\
else\
  unset colorbox
if(show_contour){
  set contour base
  set cntrparam bspline
  set style data lines
}

set view map

# PART IV : Insert custom text defined by user, if present
## Uncommented commands will be executed before plot.
 set xtics ("Jan" 15, "Feb" 45, "Mar" 74, "Apr" 105, "May" 135, "Jun" 166, "Jul" 196, "Aug" 227, "Sep" 258, "Oct" 288, "Nov" 319, "Dec" 349)
# set size ratio -1          ## Same unit length for x and y
# set lmargin at screen 0.1; set rmargin at screen 0.7  ## Leave more blank space

### Plot data as image, without interpolation between values:
 plot data_file using 1:2:3 with image notitle
# PART V : PLOT.

# PART VI : Pause if needed. Close the window by pressing q or clicking on X (see https://unix.stackexchange.com/a/485128/198901)
if (window_output) pause mouse close