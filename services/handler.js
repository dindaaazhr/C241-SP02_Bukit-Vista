const PredictAPI = require('./api.js');
const Nunjucks = require('nunjucks');

const handler = {
    predict: async (request, h) => {
        try {
            const data = request.payload;

            if (!data) {
                return {
                    status: 'FAILURE',
                    message: 'Payload is empty'
                };
            }
            const predictionResult = await PredictAPI.predict(data);
            
            function formatToRupiah(price) {
                return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR' }).format(price);
            }

            if (predictionResult.status === 'SUCCESS') {
                const renderedHtml = Nunjucks.render('index.html', {
                    result1_1: predictionResult.data.result[0].unit_id,
                    result1_2: predictionResult.data.result[0].unit_name,
                    result1_3: predictionResult.data.result[0].property_name,
                    result1_4: predictionResult.data.result[0].area_name,
                    result1_5: predictionResult.data.result[0].type_desc,
                    result1_6: predictionResult.data.result[0].total_guest_capacity,
                    result1_7: formatToRupiah(predictionResult.data.result[0].avg_price_per_day),
                    result1_8: predictionResult.data.result[0].lat,
                    result1_9: predictionResult.data.result[0].lng,

                    result2_1: predictionResult.data.result[1].unit_id,
                    result2_2: predictionResult.data.result[1].unit_name,
                    result2_3: predictionResult.data.result[1].property_name,
                    result2_4: predictionResult.data.result[1].area_name,
                    result2_5: predictionResult.data.result[1].type_desc,
                    result2_6: predictionResult.data.result[1].total_guest_capacity,
                    result2_7: formatToRupiah(predictionResult.data.result[1].avg_price_per_day),
                    result2_8: predictionResult.data.result[1].lat,
                    result2_9: predictionResult.data.result[1].lng,

                    result3_1: predictionResult.data.result[2].unit_id,
                    result3_2: predictionResult.data.result[2].unit_name,
                    result3_3: predictionResult.data.result[2].property_name,
                    result3_4: predictionResult.data.result[2].area_name,
                    result3_5: predictionResult.data.result[2].type_desc,
                    result3_6: predictionResult.data.result[2].total_guest_capacity,
                    result3_7: formatToRupiah(predictionResult.data.result[2].avg_price_per_day),
                    result3_8: predictionResult.data.result[2].lat,
                    result3_9: predictionResult.data.result[2].lng,

                    unit1: predictionResult.data.result[3].unit_id,
                    unit2: predictionResult.data.result[3].unit_name,
                    unit3: predictionResult.data.result[3].property_name,
                    unit4: predictionResult.data.result[3].area_name,
                    unit5: predictionResult.data.result[3].type_desc,
                    unit6: predictionResult.data.result[3].total_guest_capacity,
                    unit7: formatToRupiah(predictionResult.data.result[3].avg_price_per_day),
                    unit8: predictionResult.data.result[3].lat,
                    unit9: predictionResult.data.result[3].lng,
                });
                return h.response(renderedHtml).type('text/html');
            } else {
                return h.response({
                    status: 'FAILURE',
                    message: predictionResult.message
                }).code(400);
            }

        } catch (error) {
            return {
                status: 'ERROR',
                message: 'Input cannot be empty. Please provide valid data.'
            };
        }
    }
};

module.exports = handler;
