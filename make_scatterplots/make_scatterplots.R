
require(rgdal)

# file names for input maps
x_input_map_filename = "/scratch-shared/edwinhs/tristan_output/evaluation/average_global.map"
y_input_map_filename = "/scratch-shared/edwinhs/tristan_output/evaluation/bias.map"

# reading map values
x_values = readGDAL(x_input_map_filename)
y_values = readGDAL(y_input_map_filename)

# plot values
output_plot_filename = "/scratch-shared/edwinhs/tristan_output/evaluation/plot_bias.pdf"
pdf(output_plot_filename)
par(bg = "white")
plot(x_values$band1, y_values$band1)
dev.off()
