# Getting Financial Data
rm(list=ls())

requiredpackages <- c("BatchGetSymbols",  #Using Financial Data
                      "ggplot2"
)                                             

# small loop that checks whether a package needs installing and then calls the libraries
for (pkg in requiredpackages) {
  if (pkg %in% rownames(installed.packages()) == FALSE)
  {install.packages(pkg)}
  if (pkg %in% rownames(.packages()) == FALSE)
  {library(pkg, character.only = TRUE)}
}

# Set Working Directory 
setwd("/Users/agustinfaure/Desktop/Research/Machine_Learning")
getwd()

# Import GMA Data from Yahoo
# FREQ DAILY 
# set dates
first.date <- Sys.Date() - 60
last.date <- Sys.Date()
freq.data <- 'daily'

# set tickers
tickers <- c('GME')

l.out <- BatchGetSymbols(tickers = tickers, 
                         first.date = first.date,
                         last.date = last.date, 
                         freq.data = freq.data,
                         cache.folder = file.path(tempdir(), 
                                                  'BGS_Cache') ) # cache in tempdir()

# Plotting 

p <- ggplot(l.out$df.tickers, aes(x = ref.date, y = price.close))
p <- p + geom_line()
p <- p + facet_wrap(~ticker, scales = 'free_y') 
print(p)

# Save in new df and then as .csv file 
GME_daily <- l.out$df.tickers
write_csv(GME_daily, path = "GME_daily.csv")
