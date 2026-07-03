=begin
http://keto-calculator.ankerl.com/?m,161,178,08181979,m,20,25,100,1882,11242015,k

sex: 2 möglichkeiten
weight: 0 - 1500 lbs
size: 0-300cm
birthday: 1.1.1900 - 1.1.3000 (401500 tage)
expenditure: 5 möglichkeiten
(optional: custom expenditure: 0 - 5000 kcal)
bodyfat: 0-100
carbohydrate: 0-1000g
protein: 0-1000g
kcal choosen: 0-5000
start at: 401500
=end


a=2*1500*300*401500*5*5000*100*1000*1000*5000*401500

bytes = []
begin
  bytes.push a%256
  a /= 256
end while a != 0

require "base64"
bytes = bytes.pack("C*")
puts "http://keto-calculator.ankerl.com/?#{Base64.urlsafe_encode64(bytes)}"