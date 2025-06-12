"""
This script here contains functions just to test rpy2 sanity checking 
"""
# %%
# Here is a function to do addition to test rpy2
my_addition_function <- function(a, b) {
  result <- a + b
  result
}

# %%
# Here is a function that has some dataframe stuff
my_data_processing_function <- function(input_df) {
  # Perform some operations on the input data frame
  output_df <- input_df
  output_df$new_column <- rowMeans(input_df)  # Example: calculate row means
  output_df
}
