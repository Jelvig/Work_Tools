

def main():
    from Condensation import Operator
    user = Operator()
    user.basic_info()
    user.stream()
    user.insert_bins()
    user.export_ranges()

if '__name__' == main():
    main()
