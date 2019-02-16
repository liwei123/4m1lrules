from durable.lang import *

with ruleset('test'):
    #  when_all or when_any annotates antecedent
    # m represents the data to be evaluated by given rule
    @when_all(m.subject == 'World')
    def say_hello(c):
        print ('Hello {0}'.format(c.m.subject))

    # on ruleset start
    @when_start
    def start(host):
        host.post('test', { 'subject': 'World' })

#   facts (knowledge base)
#  # will be triggered by 'Kermit eats flies'
#     @when_all((m.predicate == 'eats') & (m.object == 'flies'))
#     def frog(c):
#         c.assert_fact({ 'subject': c.m.subject, 'predicate': 'is', 'object': 'frog' })
with ruleset('animal'):
    # will be triggered by 'Kermit eats flies'
    @when_all((m.predicate == 'eats') & (m.object == 'flies'))
    def frog(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'is', 'object': 'frog' })

    @when_all((m.predicate == 'eats') & (m.object == 'worms'))
    def bird(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'is', 'object': 'bird' })

    # will be chained after asserting 'Kermit is frog'
    @when_all((m.predicate == 'is') & (m.object == 'frog'))
    def green(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'is', 'object': 'green' })

    @when_all((m.predicate == 'is') & (m.object == 'bird'))
    def black(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'is', 'object': 'black' })

    @when_all(+m.subject)
    def output(c):
        print('Fact: {0} {1} {2}'.format(c.m.subject, c.m.predicate, c.m.object))

    @when_start
    def start(host):
        host.assert_fact('animal', { 'subject': 'Kermit', 'predicate': 'eats', 'object': 'flies' })

with ruleset('testing'):
    @when_all(c.first << m.t == 'deposit',
              none(m.t == 'balance'),
              c.third << m.t == 'withrawal',
              c.fourth << m.t == 'chargeback')
    def detected(c):
        print('fraud detected {0} {1} {2}'.format(c.first.t, c.third.t, c.fourth.t))


    @when_start
    def start(host):
        host.post('testing', {'t': 'deposit'})
        host.post('testing', {'t': 'withrawal'})
        host.post('testing', {'t': 'chargeback'})

with ruleset('flow'):
    # state condition uses 's'
    @when_all(s.status == 'start')
    def start(c):
        # state update on 's'
        c.s.status = 'next'
        print('start')

    @when_all(s.status == 'next')
    def next(c):
        c.s.status = 'last'
        print('next')

    @when_all(s.status == 'last')
    def last(c):
        c.s.status = 'end'
        print('last')
        # deletes state at the end
        c.delete_state()

    @when_start
    def on_start(host):
        # modifies context state
        host.patch_state('flow', { 'status': 'start' })

with ruleset('expense'):
    # use the '.' notation to match properties in nested objects
    @when_all(c.bill << (m.t == 'bill') & (m.invoice.amount > 50),
              c.account << (m.t == 'account') & (m.payment.invoice.amount == c.bill.invoice.amount))
    def approved(c):
        print ('bill amount  ->{0}'.format(c.bill.invoice.amount))
        print ('account payment amount ->{0}'.format(c.account.payment.invoice.amount))

run_all()