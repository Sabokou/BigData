--DROP PROCEDURE new_loan(INT, INT[], INT);
create or replace procedure new_loan(
    book_ids INT[]
)
language plpgsql
AS '
		DECLARE
			book INT;
			loan_id INT;
    	BEGIN

        	INSERT INTO LOAN (ts_now)
        	VALUES(now())
        	RETURNING n_loan_id INTO loan_id;
			
			
		   FOREACH book IN ARRAY $2
			LOOP
        		INSERT INTO BORROW_ITEM (n_book_id, n_loan_id)
        		VALUES (book,loan_id);
        		
   	     	WHERE n_book_id = book;
        	END loop;

        
        
		END;
	';
	
-- Test
-- CALL new_loan(1,ARRAY[1,2,3],31);

