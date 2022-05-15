let list_using_comp = list [
  entry (var ** 3)
  for (var in input_list)
  if ((var % 2) == 0)
];

let dict_using_comp = dict {
  a: 2,
  entry (var: (var ** 3))
  for (var in input_list)
  if ((var % 2) != 0),
};
