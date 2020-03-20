import axios from 'axios'

let Service = {
  getTabla: function (userId) {
        return new Promise((resolve, reject) => {
            axios.get(`http://localhost:5000/calculos/validaciones`,
              {auth: {
                username: 'a@a.com',
                password: '1234'
              }})
                .then((response) => {
                    resolve(response.data);
                }).catch(err => reject(err));
        })
    }
};
// ${process.env.TABLAS_ENDPOINT}
export default Service;
