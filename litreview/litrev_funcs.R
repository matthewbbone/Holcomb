flatten <- function(x) {
  strsplit(x, ', ')
}

flatten <- Vectorize(flatten)

key_cloud <- function(df) {
  
  flat_keys <- df %>%
    mutate(flat_keys = flatten(keywords)) %>%
    select(flat_keys)
  
  words <- unlist(flat_keys$flat_keys)
  
  keylist <- data.frame(words) %>%
    mutate(words = gsub('( |-)','',words),
           words = tolower(words)) %>%
    group_by(words) %>%
    summarize(unscaled_freq = n())%>%
    mutate(freq = ceiling(unscaled_freq^(.8))) %>%
    arrange(-freq) %>%
    select(words, freq, unscaled_freq)
  
  return(wordcloud2(keylist, 
                    color = "random-light", 
                    backgroundColor = "black", 
                    size = .8, 
                    shape = 'rectangle',
                    minRotation = 0, maxRotation = 0))
}

key_clean <- function(key) {
  key <- gsub('( |-)','',key)
  key <- tolower(key)
}

key_clean <- Vectorize(key_clean)