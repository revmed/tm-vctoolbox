# This script contains functions just to test rpy2 sanity checking

my_addition_function <- function(a, b) {
  result <- a + b
  result
}

my_data_processing_function <- function(input_df) {
  output_df <- input_df
  output_df$new_column <- rowMeans(input_df)
  output_df
}

my_df_func <- function(n) {
  data.frame(x = 1:n, y = rnorm(n))
}
