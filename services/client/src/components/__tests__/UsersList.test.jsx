import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import UsersList from '../UsersList';


const users = [
  {
    'active': true,
    'email': 'michael@email.com',
    'id': 1,
    'username': 'michael',
  },
  {
    'active': true,
    'email': 'herman@email.com',
    'id': 2,
    'username': 'herman',
  }
];

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={ users }/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.className).toBe('card card-body bg-light');
  expect(element.get(0).props.children).toBe('michael');
})

test('UsersList renders a snapshot properly', () => {
  const tree = renderer.create(<UsersList users={ users }/>).toJSON();
  expect(tree).toMatchSnapshot();
})
