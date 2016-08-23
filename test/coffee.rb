require 'loaded_die'
require 'csv'

# read path
csvfile = ARGV[0]

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
weights = coffee_data.each_with_index.map { |row,i| { i => row[1] } }.reduce(Hash.new, :merge)

# create loaded die
die = LoadedDie::Sampler.new(weights)

# roll!
outcome = die.sample

# index into coffee_data
winning_row = coffee_data[outcome]

# print result
puts "The winner is:"
puts "#{winning_row[0]} in #{winning_row[2]}"