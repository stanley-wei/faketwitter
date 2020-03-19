function changeTab(newHighlightedColor) {
  document.getElementById('tweetTab').style.color = '#8899a6';
  document.getElementById('tweetAndRepliesTab').style.color = '#8899a6';

  if(newHighlightedColor == 'tweetTab')
    document.getElementById('tweetTab').style.color = '#55ADEE';
  else if(newHighlightedColor == 'tweetAndRepliesTab')
    document.getElementById('tweetAndRepliesTab').style.color = '#55ADEE';
}
