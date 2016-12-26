require 'spec_helper'
describe 'blogAPI' do
  context 'with default values for all parameters' do
    it { should contain_class('blogAPI') }
  end
end
