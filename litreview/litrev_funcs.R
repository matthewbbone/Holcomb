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

journal_comp <- function(dat, year) {
  dat %>% 
    mutate(total = n()) %>%
    group_by(journal) %>%
    summarize(n = n(),
              perc = n() / total) %>%
    unique() %>%
    kable(format = 'markdown', title = as.character(year))
}

key_list <- function(dat) {
  
  flat_keys <- dat %>%
    mutate(flat_keys = flatten(keywords)) %>%
    select(flat_keys)
  
  words <- key_clean(unlist(flat_keys$flat_keys))
  
  keylist <- data.frame(words) %>%
    group_by(words) %>%
    summarize(count = n())
}

most_frequent <- function(dat, year, n) {
  dat %>%
    arrange(-count) %>%
    head(n) %>%
    gf_col(reorder(words, count) ~ count) %>%
    gf_labs(y = 'keyword', title = as.character(year))
}

word_cloud <- function(dat, year) {
  wc <- dat %>%
    key_cloud()
  
  title <- paste0('wc', as.character(year))
  
  saveWidget(wc, paste0(title, '.html'), selfcontained = F)
  webshot(paste0(title, '.html'), paste0(title, '.png'), vwidth=1000, vheight=900, delay=10)
}