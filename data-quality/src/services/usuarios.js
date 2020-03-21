exports.getUser = function(){
  return new Promise((resolve, reject) => {
    axios.get('localhost:500/user')
    .then(response => {
      resolve(response)
    })
    .catch(err => reject(err))

  })
}