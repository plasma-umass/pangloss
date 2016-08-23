require 'rubygems'
require 'bundler/setup'

require './my_die.rb'
require 'csv'
require 'date'
require 'sinatra'
require 'sinatra/json'

configure do
  set :CSVFILE, ARGV[0]
end

def getLocationForDate(timestamp, csvfile)
  # read CSV
  coffee_data = []
  options = {
    :headers => :first_row,
    :return_headers => false
  }

  CSV.foreach(csvfile, options) do |row|
    coffee_data << [row[0], row[1].to_i, row[2]]
  end

  # get weights
  weights = coffee_data.map { |row| row[1] }

  # create loaded die
  die = MyDie.new(timestamp, *weights)

  # roll!
  outcome = die.roll

  # index into coffee_data
  winning_row = coffee_data[outcome]

  # return result
  output = { coffee_shop: winning_row[0], location: winning_row[2], error: false, error_message: "" }
  json(output)
end

get '/' do
  getLocationForDate(Date.today.to_time.to_i, settings.CSVFILE)
end

get '/:year/:month/:day' do
  year = params[:year].to_i
  month = params[:month].to_i
  day = params[:day].to_i
  
  if year >= 1 && month >= 1 && month <= 12 && day >= 1 && day <= 31  
    ts = DateTime.new(year,month,day).to_date.to_time.to_i
    getLocationForDate(ts, settings.CSVFILE)
  else
    output = { error: true, error_message: "Invalid date." }
    json(output)
  end
end